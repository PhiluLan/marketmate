# backend/apps/integrations/serializers.py

from rest_framework import serializers
from .models import Integration, MetaIntegration

class MetaIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaIntegration
        fields = ['id', 'account_id', 'expires_at']

class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = [
            'id',
            'provider',
            'account_id',
            'access_token',
            'refresh_token',
            'expires_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
