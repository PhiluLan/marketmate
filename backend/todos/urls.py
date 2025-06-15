from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ToDoViewSet

router = DefaultRouter()
router.register(r'todos', ToDoViewSet, basename='todo')

urlpatterns = [
    # /api/todos/…
    path('', include(router.urls)),
]
