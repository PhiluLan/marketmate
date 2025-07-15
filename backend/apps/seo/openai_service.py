import openai
from django.conf import settings
from .prompts import SEO_PROMPT_TEMPLATE
from apps.seo.web_crawler import crawl_website

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def ask_openai(prompt, model="gpt-4o", max_tokens=700):
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Du bist ein SEO-Experte."},
            {"role": "user",   "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.8,
    )
    return resp.choices[0].message.content.strip()

def audit_website(url: str, first_name: str) -> str:
    crawl = crawl_website(url)
    if crawl.get("error"):
        return f"❗ Fehler beim Crawlen: {crawl['error']}"

    snippet = crawl.get("text_content", "")[:1500].replace("\n", " ")
    crawl_summary = "\n".join([
        f"- **Title**: {crawl.get('title','–')}",
        f"- **Meta-Description**: {crawl.get('meta_description','–')}",
        f"- **H1/H2**: {crawl.get('h1_count',0)}/{crawl.get('h2_count',0)}",
        f"- **Wörter**: {crawl.get('word_count',0)}",
        f"- **Content-Snippet**: {snippet}…"
    ])

    prompt = SEO_PROMPT_TEMPLATE.format(
        first_name=first_name,
        url=url,
        crawl_summary=crawl_summary
    )
    return ask_openai(prompt)
