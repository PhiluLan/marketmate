# preprocess_avazu.py
import csv, os, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from services.vector_store import VectorStore

CSV_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../data/avazu/50krecords.csv')
)

docs = []
START = 5000
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i < START:
            continue
        # kein Break hier – wir wollen bis zum Ende
        text = (
            f"user_id={row.get('id')}, "
            f"slot_id={row.get('slot_id')}, "
            f"domain={row.get('domain')}, "
            f"clicked={row.get('click')}"
        )
        docs.append({"id": f"avazu-{i}", "text": text})

print(f"Erzeuge {len(docs)} Dokumente zum Upserten…")

BATCH_SIZE = 100
total = len(docs)
for start in range(0, total, BATCH_SIZE):
    end   = min(start + BATCH_SIZE, total)
    batch = docs[start:end]
    print(f"Upserting Dokumente {start+1}–{end} von {total}…", end=" ")
    try:
        VectorStore.upsert(batch)
        print("✓")
    except Exception as e:
        print("✗")
        print(f"Fehler im Batch {start+1}–{end}:\n{e}", file=sys.stderr)
        sys.exit(1)

print("✅ Alle verbleibenden Dokumente erfolgreich upserted.")
