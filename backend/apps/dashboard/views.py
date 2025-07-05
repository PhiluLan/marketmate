from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Metric, CalendarEvent
from .serializers import MetricSerializer, CalendarEventSerializer
from datetime import timedelta
from services.llm_client import ask_lenny

class MetricListView(generics.ListAPIView):
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['type']
    ordering_fields = ['date']
    ordering = ['-date']

    def get_queryset(self):
        user = self.request.user
        queryset = Metric.objects.filter(user=user)

        # Optional: Datumsfilter per Query-Parameter
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')

        if from_date:
            queryset = queryset.filter(date__gte=from_date)
        if to_date:
            queryset = queryset.filter(date__lte=to_date)

        return queryset
    
class MetricSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')

        if not from_date or not to_date:
            return Response({'detail': 'from/to required'}, status=400)

        # Aktueller Zeitraum
        current_metrics = Metric.objects.filter(user=user, date__gte=from_date, date__lte=to_date)

        # Vergleichszeitraum: gleiche Länge, direkt davor
        from datetime import datetime
        fmt = "%Y-%m-%d"
        delta_days = (datetime.strptime(to_date, fmt) - datetime.strptime(from_date, fmt)).days + 1
        prev_from = datetime.strptime(from_date, fmt) - timedelta(days=delta_days)
        prev_to = datetime.strptime(from_date, fmt) - timedelta(days=1)

        prev_metrics = Metric.objects.filter(user=user, date__gte=prev_from, date__lte=prev_to)

        def summarize(data):
            result = {}
            for m in data:
                if m.type not in result:
                    result[m.type] = 0
                result[m.type] += m.value
            return result

        current = summarize(current_metrics)
        previous = summarize(prev_metrics)

        response = []
        for metric_type in current:
            cur = current[metric_type]
            prev = previous.get(metric_type, 0.00001)  # vermeiden: Division durch 0
            diff = ((cur - prev) / prev) * 100
            response.append({
                'type': metric_type,
                'value': round(cur, 2),
                'change_pct': round(diff, 1)
            })

        return Response(response)
    
class GoalSuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        from_date = request.query_params.get('from')
        to_date = request.query_params.get('to')
        metric_type = request.query_params.get('type', 'organic_sessions')

        if not (from_date and to_date):
            return Response({'detail': 'from/to required'}, status=400)

        metrics = Metric.objects.filter(
            user=user,
            type=metric_type,
            date__gte=from_date,
            date__lte=to_date
        ).order_by('date')

        if not metrics.exists():
            return Response({'detail': 'Keine Daten für diesen Zeitraum.'}, status=404)

        values = [m.value for m in metrics]
        total = sum(values)
        avg_daily = total / len(values)

        prompt = f"""
        Du bist ein datenbasierter Online-Marketing-Analyst.
        Die letzten {len(values)} Tage hatte der Nutzer im Durchschnitt {round(avg_daily)} {metric_type.replace('_', ' ')} pro Tag.
        Mache drei realistische Zielvorschläge für 30 Tage:
        - ein konservatives Ziel
        - ein realistisches Ziel
        - ein ambitioniertes Ziel

        Gib die Antwort bitte als Text in normalem Deutsch zurück, ohne JSON oder Bullet-Format.
        """

        try:
            result = ask_lenny(prompt)

            # Werte aus Text extrahieren
            import re
            matches = re.findall(r'([Kk]onservativ|[Rr]ealistisch|[Aa]mbitioniert):?\s*([\d.]+)', result)

            goals = {}
            for label, number in matches:
                key = label.lower()
                goals[key] = float(number.replace('.', '').replace(',', ''))

            return Response({
                'goals': goals,
                'actual': round(total),
                'daily_avg': round(avg_daily, 2),
                'text': result  # Optional: originaler Text
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
class CalendarEventViewSet(ModelViewSet):
    serializer_class = CalendarEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CalendarEvent.objects.filter(user=self.request.user).order_by('start')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

