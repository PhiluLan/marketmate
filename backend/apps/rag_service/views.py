from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.vector_store import VectorStore

class RAGQueryView(APIView):
    """
    POST /api/v1/rag/query/     { "query": "Dein Text" }
    Response: { "results": [ {...}, {...} ] }
    """
    def post(self, request):
        q = request.data.get("query", "")
        if not q:
            return Response({"error": "Feld 'query' fehlt"}, status=400)
        docs = VectorStore.query(q)
        return Response({"results": docs})
    
class RAGUpsertView(APIView):
    """
    POST /api/v1/rag/upsert/
    Request-Body: { "documents": [ { "id": "1", "text": "Inhalt A" }, ... ] }
    Response: { "upserted": <number_of_docs> }
    """
    def post(self, request):
        docs = request.data.get("documents")
        if not isinstance(docs, list) or not docs:
            return Response(
                {"error": "Bitte sende ein JSON-Feld 'documents' mit einer Liste von {id,text}-Objekten."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            VectorStore.upsert(docs)
        except Exception as e:
            return Response(
                {"error": f"Upsert fehlgeschlagen: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({"upserted": len(docs)})
