from rest_framework import serializers
from .models import Content

class ContentGenerateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[
        ('blog','Blog'),
        ('social','Social Media'),
        ('email','E-Mail'),
    ])
    tone = serializers.ChoiceField(choices=[
        ('seriös','Seriös'),
        ('locker','Locker'),
        ('technisch','Technisch'),
    ])
    length = serializers.ChoiceField(choices=[
        ('short','Kurz'),
        ('medium','Mittel'),
        ('long','Lang'),
    ])
    topic = serializers.CharField(max_length=200)

class AssetGenerateSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=200)
    n = serializers.IntegerField(default=1, min_value=1, max_value=4)
    size = serializers.ChoiceField(choices=[("256x256","256x256"),("512x512","512x512"),("1024x1024","1024x1024")], default="512x512")

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title']  # oder alle Felder, die du brauchst

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "body",
            "image",
            "ad_account_id",
            "objective",
            "daily_budget",
            "spend_cap",
            "start_time",
            "end_time",
            "attribution_spec",
        ]