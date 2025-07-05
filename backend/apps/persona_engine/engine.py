# apps/persona_engine/engine.py

import yaml
import json
from pathlib import Path
from services.openai_client import chat_completion

class PersonaEngine:
    """
    Lädt System-Prompts aus YAML, baut Chat-Nachrichten-Listen für OpenAI
    zusammen und hält Function-Schemas bereit für automatisierte Action-Calls.
    """

    def __init__(self, persona_name: str = "Lenny"):
        self.persona_name    = persona_name
        self.prompt_data     = self._load_prompt(persona_name)
        self.function_schemas = self._load_functions()

    def _load_prompt(self, name: str) -> dict:
        """
        Liest das System-Prompt aus prompts/system.yaml ein.
        """
        base        = Path(__file__).parent
        prompt_path = base / "prompts" / "system.yaml"
        with prompt_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _load_functions(self) -> list[dict]:
        """
        Lädt alle JSON-Schemas aus dem functions/-Ordner.
        """
        base          = Path(__file__).parent
        functions_dir = base / "functions"
        schemas       = []

        for json_file in functions_dir.glob("*.json"):
            with json_file.open(encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    schemas.extend(data)
                else:
                    schemas.append(data)

        return schemas

    def build_messages(
        self,
        user_input: str,
        *,
        rag_texts: str | None = None,
        summary: bool = False
    ) -> list[dict]:
        """
        Baut die Message-Liste:
        1) Immer ein System-Prompt (aus YAML)
        2) Optional: RAG-Kontext + Zusammenfassungs-Anweisung
        3) Dann die User-Nachricht
        """

        # 1) Baue das System-Prompt aus self.prompt_data
        pd = self.prompt_data
        system_text = (
            f"Persona: {pd['persona']}\n"
            f"Beschreibung:\n{pd['description']}\n\n"
            f"Style-Guide:\n"
            f"  Tone: {pd['style_guide']['tone']}\n"
            f"  Format: {pd['style_guide']['format']}"
        )

        messages = [
            {"role": "system", "content": system_text}
        ]

        # 2) Wenn RAG-Texte vorliegen und eine Zusammenfassung gewünscht ist
        if rag_texts and summary:
            messages.append({
                "role": "system",
                "content": (
                    "Du hast gerade diese Daten aus dem Website-Crawl erhalten:\n\n"
                    f"{rag_texts}\n\n"
                    "Erstelle daraus eine **vollständige**, gut leserliche Zusammenfassung "
                    "(keine Aufzählungspunkte, sondern zusammenhängender Fließtext), "
                    "maximal 200 Wörter."
                )
            })

        # 3) Füge zum Schluss die User-Nachricht an
        messages.append({
            "role": "user",
            "content": user_input
        })

        return messages

    def chat(self, user_input: str, stream: bool = False, **kwargs) -> dict:
        """
        Komfort-Methode: Baut messages, lädt Function-Schemas und ruft OpenAI auf.
        Gibt das rohe JSON-Response zurück, damit Function-Calling ausgewertet
        werden kann.
        """
        messages = self.build_messages(user_input)
        return chat_completion(
            messages=messages,
            functions=self.function_schemas,
            function_call="auto",
            stream=stream,
            **kwargs
        )
