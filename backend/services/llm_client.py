# backend/services/llm_client.py

from apps.persona_engine.engine import PersonaEngine

def ask_lenny(user_input: str, *, stream: bool = False, **kwargs) -> str:
    """
    Fragt Lenny (unsere Persona) etwas und gibt die reine Text-Antwort zurück.

    :param user_input: Die Eingabe, die Lenny verstehen soll.
    :param stream:     Ob wir streaming wollen (derzeit nur False supported).
    :param kwargs:     Weitere OpenAI-Parameter (temperature, max_tokens, …).
    :return:           Der Text, den Lenny geantwortet hat.
    """
    engine = PersonaEngine(persona_name="Lenny")
    # Gibt das rohe JSON zurück mit choices[].message
    raw = engine.chat(user_input, stream=stream, **kwargs)

    # Extrahiere aus raw das assistant-Message-Objekt
    choice = raw["choices"][0]["message"]

    # Wenn eine Funktion aufgerufen werden sollte, geben wir das komplett zurück
    if choice.get("function_call"):
        return choice

    # Sonst geben wir nur den Content-String zurück
    return choice.get("content", "")
