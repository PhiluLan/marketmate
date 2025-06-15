from rest_framework import serializers
from .models import SEOAudit
from websites.models import Website

class SEOAuditSerializer(serializers.ModelSerializer):
    website = serializers.PrimaryKeyRelatedField(
        queryset=Website.objects.all()
    )

    class Meta:
        model = SEOAudit
        fields = [
            'id',
            'website',
            'score',
            'load_time',
            'broken_links',
            'created_at',
            'meta_title',
            'meta_description',
            'meta_robots',
            'canonical',
            'h1_count',
            'h2_count',
            'word_count',
            'og_title',
            'og_description',
            'http_status',
            'robots_txt_found',
            'robots_txt_content',
            'sitemap_found',
            'sitemap_url',
            'fcp',
            'lcp',
            'cls',
            'tti',
            'ssl_valid_until','cipher_strength','hsts','csp',
            # robots.txt & Sitemap
            'robots_directives',
            'sitemap_valid',
            'sitemap_errors',
            # Title-Tag-Check
            'title_length',
            'title_keyword_position',
            'meta_description_length',
            'meta_description_unique',
            'h3_count',
            'h4_count',
            'h5_count',
            'h6_count',
            'reading_score',
            'keyword_density',
            'duplicate_sections',
            'backlink_count',
            'referring_domains',
            'domain_authority',
            'trust_score',
            'anchor_text_distribution',

        ]
