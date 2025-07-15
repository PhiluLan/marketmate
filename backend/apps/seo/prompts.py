# backend/seo/prompts.py

def meta_description_prompt(website_name, website_topic):
    return (
        f"Schreibe eine professionelle und ansprechende Meta-Description für die Webseite '{website_name}', "
        f"die sich mit dem Thema '{website_topic}' beschäftigt. Die Beschreibung soll maximal 160 Zeichen lang sein, neugierig machen und zum Klicken animieren."
    )

def title_prompt(website_name, website_topic):
    return (
        f"Erstelle einen einprägsamen SEO-Titel für die Seite '{website_name}' zum Thema '{website_topic}'. Maximal 60 Zeichen."
    )

SEO_PROMPT_TEMPLATE = """
Hey {first_name}! Hier ist dein erster heyLenny Check von {url}!

Du bist ein erfahrener SEO-Experte und berichtest in einem lockeren, reißerischen Stil.
Nutze die folgenden Crawler-Infos, um:

{crawl_summary}

– die größten Baustellen **knallhart** aufzudecken,  
– in knackigen Bullet-Points die Top-3-Optimierungen zu nennen,  
– und zum Schluss in 2–3 Sätzen das Geschäftsmodell und die Core-Actionables zusammenzufassen.  
"""
