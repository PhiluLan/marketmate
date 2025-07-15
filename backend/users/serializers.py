from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password     = serializers.CharField(write_only=True)
    role         = serializers.CharField(required=False, default='user')
    first_name   = serializers.CharField(required=True)
    last_name    = serializers.CharField(required=True)
    website_url  = serializers.URLField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'role',
            'first_name',
            'last_name',
            'website_url',
            'company_name', 
            'industry',
            'instagram_url',
            'facebook_url',
            'linkedin_url'
        )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
