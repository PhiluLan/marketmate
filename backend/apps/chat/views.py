# backend/apps/chat/views.py

import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from apps.persona_engine.engine import PersonaEngine
from services.openai_client import chat_completion
from services.vector_store import VectorStore
from apps.memory_service.service import MemoryService

from apps.seo.web_crawler import crawl_website          # ← neu
from apps.seo.tasks import task_deep_crawl_and_index, task_seo_audit
from apps.ads.services.facebook_ads_service import create_meta_ad_campaign


@method_decorator(csrf_exempt, name="dispatch")
class ChatAPIView(APIView):
    permission_classes = []

    def post(self, request):
        user_input = (request.data.get("message") or "").strip()
        if not user_input:
            return Response(
                {"error": "Bitte sende ein Feld 'message' mit deinem Text."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lower = user_input.lower()
        url_match = re.search(r"(https?://[^\s]+)", user_input)

        # ─── 1) Direkte Zusammenfassung einer URL ─────────────────────────────
        if lower.startswith("zusammenfassung von") and url_match:
            url = url_match.group(1)
            # 1a) synchron crawlen
            result = crawl_website(url)
            if result.get("error"):
                return Response(
                    {"error": f"Crawl-Fehler: {result['error']}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 1b) Kontexttext zusammenbauen
            context = "\n".join([
                f"Title: {result.get('title','')}",
                f"Meta-Description: {result.get('meta_description','')}",
                f"H1 Count: {result.get('h1_count')}",
                f"H2 Count: {result.get('h2_count')}",
                f"Wortanzahl: {result.get('word_count')}",
            ])

            # 1c) Chat-Prompt für Zusammenfassung
            engine = PersonaEngine("Lenny")
            messages = engine.build_messages(
                user_input,
                rag_texts=context,
                summary=True
            )
            ai_text = chat_completion(messages)
            return Response({"response": ai_text})


        # ─── 2) URL-Crawl (asynchron für späteren RAG) ─────────────────────────
        if url_match:
            url = url_match.group(1)
            task_deep_crawl_and_index.delay(url)
            return Response({
                "response": (
                    f"Alles klar! Ich crawle gerade `{url}` und indexiere die wichtigsten Inhalte. "
                    "Gib mir nach 10–20 Sekunden Bescheid und frag dann: „Zusammenfassung von <URL>“"
                )
            })

        # ─── 3) SEO-Audit triggern ─────────────────────────────────────────────
        if lower.startswith("audit "):
            parts = user_input.split()
            if len(parts) >= 2 and parts[1].isdigit():
                task_seo_audit.delay(int(parts[1]))
                return Response({"response": f"Starte SEO-Audit für Website #{parts[1]}…"})

        # ─── 4) RAG oder normale Chat/Function-Calling ──────────────────────────
        user = request.user if request.user.is_authenticated else None
        conv = MemoryService.get_or_create_conversation(user)
        MemoryService.append_message(conv, "user", user_input)

        rag_docs = VectorStore.query(user_input, top_k=5)
        engine   = PersonaEngine("Lenny")

        if rag_docs:
            context = "\n\n".join(d["text"] for d in rag_docs)
            messages = engine.build_messages(user_input)
            messages.insert(1, {
                "role": "system",
                "content": f"Ich habe Folgendes aus dem Crawl gefunden:\n{context}"
            })
            ai_text = chat_completion(messages)
            MemoryService.append_message(conv, "assistant", ai_text)
            return Response({"response": ai_text})

        # Function-Calling Flow für Meta-Ads
        messages = engine.build_messages(user_input)
        raw = chat_completion(
            messages=messages,
            functions=engine.function_schemas,
            function_call="auto"
        )
        choice = raw["choices"][0]["message"]

        if choice.get("function_call"):
            fn_name = choice["function_call"]["name"]
            args    = json.loads(choice["function_call"]["arguments"])
            try:
                if fn_name == "create_meta_ad_campaign":
                    result = create_meta_ad_campaign(**args)
                else:
                    raise ValueError(f"Unbekannte Funktion: {fn_name}")

                summary = (
                    f"Kampagne „{args.get('campaign_name')}“ "
                    f"(ID: {result.get('id')}) wurde erfolgreich erstellt."
                )
                MemoryService.append_message(conv, "assistant", summary)
                return Response({"response": summary, "details": result})

            except Exception as e:
                return Response(
                    {"error": f"Fehler beim Funktionsaufruf: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # normale Chat-Antwort
        text = choice.get("content", "")
        MemoryService.append_message(conv, "assistant", text)
        return Response({"response": text})


@method_decorator(csrf_exempt, name="dispatch")
class ChatStreamView(APIView):
    def post(self, request):
        return Response(
            {"error": "Streaming mit Function Calling nicht unterstützt."},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
