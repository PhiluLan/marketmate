import openai
from django.conf import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def ask_openai(prompt, model="gpt-4o", max_tokens=400):
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein SEO-Experte."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return chat_completion.choices[0].message.content.strip()
