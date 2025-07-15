# backend/seo/models.py

from django.db import models
from websites.models import Website

# backend/seo/models.py

from django.db import models
from websites.models import Website

class SEOAudit(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    load_time = models.IntegerField(default=0)
    broken_links = models.IntegerField(default=0)

    # NEU: SEO-Daten
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_robots = models.CharField(max_length=128, null=True, blank=True)
    meta_hreflang = models.CharField(max_length=128, null=True, blank=True)
    canonical = models.CharField(max_length=255, null=True, blank=True)
    og_title = models.CharField(max_length=255, null=True, blank=True)
    og_description = models.TextField(null=True, blank=True)
    twitter_card = models.CharField(max_length=128, null=True, blank=True)
    twitter_description = models.TextField(null=True, blank=True)
    h1_count = models.IntegerField(blank=True, null=True)
    h2_count = models.IntegerField(blank=True, null=True)
    word_count = models.IntegerField(blank=True, null=True)
    http_status = models.IntegerField(null=True, blank=True)
    robots_txt_found = models.BooleanField(null=True, default=False)
    robots_txt_content = models.TextField(null=True, blank=True)
    sitemap_found = models.BooleanField(null=True, default=False)
    sitemap_url = models.CharField(max_length=255, null=True, blank=True)
    # === Core Web Vitals ===
    fcp = models.FloatField(null=True, blank=True, help_text="First Contentful Paint in ms")
    lcp = models.FloatField(null=True, blank=True, help_text="Largest Contentful Paint in ms")
    cls = models.FloatField(null=True, blank=True, help_text="Cumulative Layout Shift")
    tti = models.FloatField(null=True, blank=True, help_text="Time To Interactive in ms")

        # ── Neue Social-Media-Felder ───────────────────────────
    instagram_followers    = models.IntegerField(null=True, blank=True)
    instagram_avg_likes    = models.IntegerField(null=True, blank=True)
    instagram_avg_comments = models.IntegerField(null=True, blank=True)

    facebook_followers     = models.IntegerField(null=True, blank=True)
    facebook_avg_likes     = models.IntegerField(null=True, blank=True)
    facebook_avg_comments  = models.IntegerField(null=True, blank=True)

    linkedin_followers     = models.IntegerField(null=True, blank=True)
    linkedin_avg_likes     = models.IntegerField(null=True, blank=True)
    linkedin_avg_comments  = models.IntegerField(null=True, blank=True)
    # ─────────────────────────────────────────────────────────
    redirect_chain_length = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der Redirects bis zum finalen Ziel"
    )
    redirect_loop = models.BooleanField(
        null=True, blank=True, default=False,
        help_text="True, wenn eine Redirect-Schleife erkannt wurde"
    )
    ssl_valid_until = models.DateTimeField(
        null=True, blank=True,
        help_text="Gültigkeitsende des SSL/TLS-Zertifikats"
    )
    cipher_strength = models.CharField(
        max_length=64, null=True, blank=True,
        help_text="Cipher-Stärke des SSL/TLS-Zertifikats"
    )
    hsts = models.BooleanField(
        null=True, blank=True, default=False,
        help_text="Strict-Transport-Security-Header vorhanden"
    )
    csp = models.BooleanField(
        null=True, blank=True, default=False,
        help_text="Content-Security-Policy-Header vorhanden"
    )
    robots_directives = models.TextField(
        null=True, blank=True,
        help_text="Gefundene Direktiven aus robots.txt"
    )
    sitemap_valid = models.BooleanField(
        null=True, blank=True, default=False,
        help_text="True, wenn sitemap.xml gültiges XML ist"
    )
    sitemap_errors = models.TextField(
        null=True, blank=True,
        help_text="Fehler bei Sitemap-Parsing"
    )
    js_render_blocking_resources = models.TextField(
    null=True, blank=True,
    help_text="Liste der clientseitig geladenen JavaScript-Ressourcen"
    )
    # === Title-Tag-Check ===
    title_length = models.IntegerField(
        null=True, blank=True,
        help_text="Länge des <title>-Tags in Zeichen"
    )
    title_keyword_position = models.IntegerField(
        null=True, blank=True,
        help_text="1-basierte Position des primären Keywords im Title, 0 wenn nicht gefunden"
    ) 
    meta_description_length = models.IntegerField(
        null=True, blank=True,
        help_text="Länge der Meta-Description in Zeichen"
    )
    meta_description_unique = models.BooleanField(
        null=True, blank=True, default=True,
        help_text="True, wenn Meta-Description nicht in älteren Audits vorhanden"
    )  
        # === Überschriften-Struktur (H3–H6) ===
    h3_count = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der <h3>-Überschriften"
    )
    h4_count = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der <h4>-Überschriften"
    )
    h5_count = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der <h5>-Überschriften"
    )
    h6_count = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der <h6>-Überschriften"
    )
        # === Content-Qualität & Lesbarkeit ===
    reading_score = models.FloatField(
        null=True, blank=True,
        help_text="Flesch-Reading-Ease Score"
    )
    keyword_density = models.FloatField(
        null=True, blank=True,
        help_text="Keyword-Dichte in Prozent (Anteil Keyword/Wortanzahl)"
    )
        # === Duplicate-Content (Intra-Site) ===
    duplicate_sections = models.TextField(
        null=True, blank=True,
        help_text="Wiederholt vorkommende Sätze oder Absätze"
    )
        # === Off-Page: Backlinks & Referring Domains ===
    backlink_count = models.IntegerField(
        null=True, blank=True,
        help_text="Geschätzte Gesamtzahl der Backlinks (externe Links)"
    )
    referring_domains = models.IntegerField(
        null=True, blank=True,
        help_text="Anzahl der einzigartigen Domains, die verlinken"
    )
        # === Off-Page: Domain Authority & Trust Score ===
    domain_authority = models.FloatField(
        null=True, blank=True,
        help_text="Domain Authority (Moz)"
    )
    trust_score = models.FloatField(
        null=True, blank=True,
        help_text="Spam Score (Moz)"
    )
        # === Off-Page: Ankertext-Verteilung ===
    anchor_text_distribution = models.TextField(
        null=True, blank=True,
        help_text="JSON-Array der Top-Ankertexte mit Häufigkeiten"
    )


    # ... Du kannst beliebig viele weitere Felder ergänzen!



    def __str__(self):
        return f"Audit {self.id} für {self.website} @ {self.created_at}"
