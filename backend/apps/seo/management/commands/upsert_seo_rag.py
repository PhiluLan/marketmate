# backend/apps/seo/management/commands/upsert_seo_rag.py

import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from websites.models import Website
from keywords.models import Keyword, KeywordRanking
from apps.seo.models import SEOAudit
from services.vector_store import VectorStore

class Command(BaseCommand):
    help = "Upsert SEO-Audit- und Keyword-Ranking-Daten in Pinecone für RAG"

    def handle(self, *args, **options):
        docs = []

        # 1) SEO-Audit-Daten
        for audit in SEOAudit.objects.select_related('website').all():
            site = audit.website
            text = (
                f"SEO-Audit für {site.url}\n"
                f"Datum: {audit.created_at.date()}\n"
                f"Score: {audit.score}\n"
                f"Ladezeit (ms): {audit.load_time}\n"
                f"Broken Links: {audit.broken_links}\n"
            )
            docs.append({
                "id": f"seo-audit-{audit.id}",
                "text": text
            })

        # 2) Keyword-Ranking-Historie (letzte 30 Tage)
        cutoff = datetime.date.today() - datetime.timedelta(days=30)
        for kw in Keyword.objects.select_related('website').all():
            recent_rankings = KeywordRanking.objects.filter(
                keyword=kw,
                checked_at__date__gte=cutoff
            ).order_by('checked_at')
            if not recent_rankings.exists():
                continue

            entries = "\n".join(
                f"{r.checked_at.date()}: Rang {r.rank}"
                for r in recent_rankings
            )
            docs.append({
                "id": f"kw-{kw.id}",
                "text": (
                    f"Keyword: {kw.keyword}\n"
                    f"Webseite: {kw.website.url}\n"
                    f"Ranking-Historie (letzte 30 Tage):\n{entries}"
                )
            })

        # 3) Upsert in Pinecone
        self.stdout.write(f"Upserting {len(docs)} Dokumente in Pinecone…")
        try:
            VectorStore.upsert(docs)
            self.stdout.write(self.style.SUCCESS(f"Upserted {len(docs)} docs successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Upsert fehlgeschlagen: {e}"))
            raise SystemExit(1)
