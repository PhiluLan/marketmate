from django.core.management.base import BaseCommand
from seo.models import SEOAudit, Website
from seo.services.seo_crawler import run_seo_audit

class Command(BaseCommand):
    help = 'Starte einen SEO-Audit für eine Website und speichere das Ergebnis.'

    def add_arguments(self, parser):
        parser.add_argument('website_id', type=int, help='ID der Website in der DB')

    def handle(self, *args, **options):
        website_id = options['website_id']
        audit = run_seo_audit(website_id)
        self.stdout.write(f"SEO-Audit #{audit.pk} für Website {website_id} abgeschlossen")

        audit = SEOAudit.objects.create(
            website=website,
            score=result['score'],
            load_time=result['load_time'],
            broken_links=result['broken_links']
        )
        self.stdout.write(self.style.SUCCESS(f'Audit #{audit.id} erstellt'))
