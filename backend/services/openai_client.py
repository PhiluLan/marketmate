# backend/services/openai_client.py

import os
import openai

# API-Key aus .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default-Modelle (kann via ENV überschrieben werden)
DEFAULT_CHAT_MODEL      = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
DEFAULT_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")


def chat_completion(
    messages: list[dict],
    model_name: str | None    = None,
    temperature: float        = 0.7,
    max_tokens: int           = 300,
    functions: list | None    = None,
    function_call: str | dict = None,
    **kwargs
) -> dict:
    """
    Wrapper für openai.chat.completions.create:
    - messages
    - temperature, max_tokens, …
    - functions + function_call (Function Calling)
    - alle weiteren Params via **kwargs

    Gibt das rohe Response-Objekt als Dict zurück.
    """
    model = model_name or DEFAULT_CHAT_MODEL

    params: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if functions is not None:
        params["functions"] = functions
    if function_call is not None:
        params["function_call"] = function_call

    # zusätzliche Parameter (z.B. stop, top_p, usw.)
    params.update(kwargs)

    # Ab v1.0.0+ Interface
    response = openai.chat.completions.create(**params)
    return response.to_dict()  # Rückgabe als reines Dict


def chat_stream(
    messages: list[dict],
    model_name: str | None    = None,
    temperature: float        = 0.7,
    functions: list | None    = None,
    function_call: str | dict = None,
    **kwargs
):
    """
    Streaming-Wrapper für tokenweise Ausgabe.
    Unterstützt ebenfalls Function Calling.
    Yields jeweils das nächste Delta-Token als String.
    """
    model = model_name or DEFAULT_CHAT_MODEL

    params: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
    }

    if functions is not None:
        params["functions"] = functions
    if function_call is not None:
        params["function_call"] = function_call

    params.update(kwargs)

    # Streaming-Call
    response = openai.chat.completions.create(**params)
    for chunk in response:
        # delta enthält das nächste Fragment
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            yield delta


def create_embeddings(
    texts: str | list[str],
    model_name: str | None = None,
    **kwargs
) -> list[list[float]]:
    """
    Wrapper für openai.embeddings.create (v1.0.0+).
    - texts: String oder Liste von Strings
    - Zusätzliche Params via **kwargs
    Rückgabe: Liste von Embedding-Vektoren.
    """
    model = model_name or DEFAULT_EMBEDDING_MODEL
    params = {
        "model": model,
        "input": texts,
    }
    params.update(kwargs)

    response = openai.embeddings.create(**params)
    return [datum.embedding for datum in response.data]
