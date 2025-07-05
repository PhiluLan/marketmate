# upload_feature_mapping.py

from dotenv import load_dotenv
import os

# 1) .env laden, damit VectorStore den API-Key liest
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from services.vector_store import VectorStore



# 2) Mapping definieren
feature_docs = [
    {
        "id": "avazu-feature-slot_id",
        "text": "slot_id bezeichnet die Position des Banners auf der Seite, z.B. 1=oben, 2=rechts oben."
    },
    {
        "id": "avazu-feature-domain",
        "text": "domain ist die Publisher-Domain, auf der die Anzeige ausgeliefert wurde."
    },
    {
        "id": "avazu-feature-click",
        "text": "click ist das Klick-Label: 1 = geklickt, 0 = kein Klick."
    },
    {
        "id": "avazu-feature-C14",
        "text": "C14 steht für Altersgruppe, Kategorien: 1=18–24, 2=25–34, 3=35–44, 4=45+."
    },
    # … für C15…C21 analog …
]

# 3) Upsert in Pinecone
print(f"Upserting {len(feature_docs)} Feature-Mapping-Dokumente…")
VectorStore.upsert(feature_docs)
print("✅ Feature-Mappings erfolgreich upserted.")
