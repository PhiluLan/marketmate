from django.urls import path
from .views import RAGQueryView, RAGUpsertView

urlpatterns = [
    path('query/', RAGQueryView.as_view(), name='rag-query'),
    path('upsert/', RAGUpsertView.as_view(), name='rag-upsert'),
]
