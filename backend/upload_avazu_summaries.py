# upload_avazu_summaries.py

import csv, os, sys
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from services.vector_store import VectorStore

# Pfad zur Avazu-CSV
CSV_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../data/avazu/50krecords.csv')
)

# Aggregate sammeln
ctr_per_slot   = defaultdict(lambda: [0,0])
ctr_per_domain = defaultdict(lambda: [0,0])

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        slot = row.get('slot_id')
        dom  = row.get('domain')
        clk  = int(row.get('click', 0))
        ctr_per_slot[slot][0]   += clk;   ctr_per_slot[slot][1]   += 1
        ctr_per_domain[dom][0]  += clk;   ctr_per_domain[dom][1]  += 1

# Summary-Dokumente erstellen
docs = []

# Slot-Summary
slot_lines = [
    f"Position {slot}: { (clicks/imps)*100 if imps else 0:.2f}% CTR ({clicks}/{imps})"
    for slot,(clicks,imps) in ctr_per_slot.items()
]
docs.append({
    "id": "avazu-summary-slot",
    "text": "CTR pro Banner-Position (Avazu Sample):\n" + "\n".join(slot_lines)
})

# Top-5-Domain-Summary
top_domains = sorted(
    ctr_per_domain.items(),
    key=lambda kv: kv[1][1],
    reverse=True
)[:5]
dom_lines = [
    f"{dom}: { (clicks/imps)*100 if imps else 0:.2f}% CTR ({clicks}/{imps})"
    for dom,(clicks,imps) in top_domains
]
docs.append({
    "id": "avazu-summary-domain",
    "text": "Top 5 Domains nach Impressionen und deren CTR:\n" + "\n".join(dom_lines)
})

# Upsert in Pinecone
print(f"Upserting {len(docs)} Summary-Dokumente…")
try:
    VectorStore.upsert(docs)
    print("✅ Summaries erfolgreich upserted.")
except Exception as e:
    print(f"❌ Fehler beim Upsert: {e}", file=sys.stderr)
    sys.exit(1)
