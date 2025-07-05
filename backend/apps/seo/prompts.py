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

# Hier kannst du nach Bedarf weitere Prompt-Funktionen hinzufügen:
# z.B. für Produkttexte, Social Media Posts etc.
