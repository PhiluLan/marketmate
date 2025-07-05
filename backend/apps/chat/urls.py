# backend/apps/chat/urls.py

from django.urls import path
from .views import ChatAPIView, ChatStreamView

urlpatterns = [
    path('', ChatAPIView.as_view(), name='chat'),
    path('stream/', ChatStreamView.as_view(), name='chat-stream'),
]
