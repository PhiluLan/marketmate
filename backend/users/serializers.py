from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Passwort nur beim Schreiben erlauben, nicht beim Lesen
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False, default='user')   # HINZUGEFÜGT!

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
