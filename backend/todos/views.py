from rest_framework import viewsets, permissions
from .models import ToDo
from .serializers import ToDoSerializer

class ToDoViewSet(viewsets.ModelViewSet):
    """
    Aus:
    - GET    /api/todos/        → Liste aller ToDos des eingeloggten Users
    - POST   /api/todos/        → Neues ToDo anlegen
    - GET    /api/todos/{id}/   → Einzelnes ToDo anzeigen
    - PUT    /api/todos/{id}/   → ToDo updaten
    - PATCH  /api/todos/{id}/   → ToDo teilweise bearbeiten
    - DELETE /api/todos/{id}/   → ToDo löschen
    """
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Jeder User sieht nur seine eigenen ToDos
        return ToDo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Beim Erstellen setzen wir automatisch das user-Feld auf request.user
        serializer.save(user=self.request.user)
