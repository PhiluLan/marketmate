from rest_framework import serializers
from .models import Keyword, KeywordRanking, KeywordMetrics
from websites.models import Website

class KeywordRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordRanking
        fields = ('id', 'rank', 'checked_at')

class KeywordSerializer(serializers.ModelSerializer):
    website = serializers.PrimaryKeyRelatedField(queryset=Website.objects.all())
    latest = KeywordRankingSerializer(many=True, read_only=True)

    class Meta:
        model = Keyword
        fields = ['id', 'term', 'region', 'created_at']

class KeywordMetricsSerializer(serializers.ModelSerializer):
    """
    Neue Serializer-Klasse für dein KeywordMetrics-Modell.
    """
    class Meta:
        model = KeywordMetrics
        fields = ['keyword', 'monthly_searches', 'competition', 'low_cpc', 'high_cpc', 'last_updated']

# Neuer Serializer für die öffentliche Keyword-Analyse
class KeywordIdeaSerializer(serializers.Serializer):
    keyword           = serializers.CharField(max_length=255)
    region            = serializers.CharField(max_length=10, allow_blank=True)
    monthly_searches  = serializers.IntegerField()
    competition       = serializers.CharField(max_length=10)
    low_cpc           = serializers.FloatField()
    high_cpc          = serializers.FloatField()

class DomainRankingSerializer(serializers.Serializer):
    keyword     = serializers.CharField()
    position    = serializers.FloatField(allow_null=True)
    impressions = serializers.IntegerField()
    clicks      = serializers.IntegerField()
    source      = serializers.CharField()

class CompetitorRankingSerializer(serializers.Serializer):
    keyword  = serializers.CharField()
    domain   = serializers.CharField()
    position = serializers.IntegerField(allow_null=True)
    url      = serializers.URLField(allow_null=True)

class SERPResultSerializer(serializers.Serializer):
    title   = serializers.CharField()
    link    = serializers.URLField()
    snippet = serializers.CharField()
