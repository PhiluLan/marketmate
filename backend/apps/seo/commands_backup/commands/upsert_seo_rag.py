# backend/seo/management/commands/upsert_seo_rag.py

import datetime
from django.core.management.base import BaseCommand
from seo.models import SEOAudit
from keywords.models import Keyword
from services.vector_store import VectorStore

class Command(BaseCommand):
    help = "Upsert SEO-Audit- und Keyword-Ranking-Daten in Pinecone für RAG"

    def handle(self, *args, **options):
        docs = []

        # 1) SEO-Audit-Daten (funktioniert mit select_related)
        for audit in SEOAudit.objects.select_related('website').all():
            site = audit.website
            text = (
                f"SEO-Audit für {site.url}\n"
                f"Datum: {audit.created_at.date()}\n"
                f"Score: {audit.score}\n"
                f"Ladezeit (ms): {audit.load_time}\n"
                f"Broken Links: {audit.broken_links}\n\n"
                f"Meta-Title: {audit.meta_title}\n"
                f"Meta-Description: {audit.meta_description}\n"
                f"FCP: {audit.fcp} ms, LCP: {audit.lcp} ms, CLS: {audit.cls}\n"
            )
            docs.append({
                "id": f"seo-audit-{audit.id}",
                "text": text
            })

        # 2) Keyword-Ranking-Historie (letzte 30 Tage) ohne select_related
        cutoff = datetime.date.today() - datetime.timedelta(days=30)
        for kw in Keyword.objects.all():
            # über das related_name 'rankings' des KeywordRanking-Modells
            recent_rankings = kw.rankings.filter(
                checked_at__date__gte=cutoff
            ).order_by('checked_at')

            if not recent_rankings.exists():
                continue

            history = "\n".join(
                f"{r.checked_at.date()}: Rang {r.rank}"
                for r in recent_rankings
            )
            docs.append({
                "id": f"kw-{kw.id}",
                "text": (
                    f"Keyword: {kw.term} (Region: {kw.region})\n"
                    f"Ranking-Historie (letzte 30 Tage):\n{history}"
                )
            })

        # 3) Upsert in Pinecone
        total = len(docs)
        self.stdout.write(f"Upserting {total} Dokumente in Pinecone…")
        try:
            VectorStore.upsert(docs)
            self.stdout.write(self.style.SUCCESS(f"✅ Erfolgreich {total} Dokumente upserted."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Upsert fehlgeschlagen: {e}"))
            raise SystemExit(1)
