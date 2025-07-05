# apps/content/services/openai_client.py

from openai import OpenAI
from django.conf import settings

# Neuen Client instanziieren
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_content(format_type, tone, length, topic):
    prompt = (
        f"Erstelle einen {format_type}-Text zum Thema '{topic}' "
        f"im {tone}-Stil und einer Länge von {length}."
    )
    # Nutzung des instanzierten Clients
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
