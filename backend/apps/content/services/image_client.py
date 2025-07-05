# apps/content/services/image_client.py

import openai
from django.conf import settings

# API-Key setzen
openai.api_key = settings.OPENAI_API_KEY

def generate_image(prompt: str, n: int = 1, size: str = "512x512"):
    """
    Ruft den OpenAI-Bild-Endpunkt (DALL·E) auf.
    Gibt eine Liste von URL-Strings zurück.
    """
    # Bild generieren
    response = openai.images.generate(
        prompt=prompt,
        n=n,
        size=size
    )

    # response ist ein ImagesResponse-Objekt => nutze response.data und .url
    return [img.url for img in response.data]
