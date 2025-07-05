from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetricListView
from .views import MetricSummaryView
from .views import GoalSuggestionView
from .views import CalendarEventViewSet

router = DefaultRouter()
router.register('calendar-events', CalendarEventViewSet, basename='calendar-events')

urlpatterns = [
    path('', include(router.urls)),
    path('metrics/', MetricListView.as_view(), name='metric-list'),
    path('metrics/summary/', MetricSummaryView.as_view(), name='metric-summary'),
    path('metrics/goals/', GoalSuggestionView.as_view(), name='goal-suggestion')
]
