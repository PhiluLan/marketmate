#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# 1) .env laden
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from services.vector_store import VectorStore



# 2) Token und Ad-Account aus der .env oder hartkodiert
TOKEN = (os.getenv("FB_SYSTEM_TOKEN") or os.getenv("FB_ACCESS_TOKEN") or "").strip()
ACCOUNT = "act_3916526251934359"  # deine Ad-Account-ID (mit Prefix act_)

if not TOKEN:
    print("❌ Kein FB_SYSTEM_TOKEN und kein FB_ACCESS_TOKEN in der Umgebung gefunden.", file=sys.stderr)
    sys.exit(1)

# 3) Ads + Insights abrufen
url = f"https://graph.facebook.com/v17.0/{ACCOUNT}/ads"
params = {
    "access_token": TOKEN,
    "fields": "id,name,insights.limit(1){impressions,clicks,spend}",
    "limit": 50
}

resp = requests.get(url, params=params)
if resp.status_code != 200:
    print(f"❌ Facebook-API-Error {resp.status_code}: {resp.text}", file=sys.stderr)
    sys.exit(1)

ads = resp.json().get("data", [])
if not ads:
    print("⚠️  Keine Ads gefunden.", file=sys.stderr)
    sys.exit(0)

# 4) Dokumente für Pinecone erzeugen
docs = []
for ad in ads:
    ins = ad.get("insights", {}).get("data", [{}])[0]
    text = (
        f"Ad-ID: {ad['id']}\n"
        f"Name: {ad.get('name','–')}\n"
        f"Impressions: {ins.get('impressions','–')}, "
        f"Clicks: {ins.get('clicks','–')}, "
        f"Spend: CHF {ins.get('spend','–')}"
    )
    docs.append({"id": ad["id"], "text": text})

# 5) Upsert in Pinecone
print(f"Upserting {len(docs)} Ads…")
try:
    VectorStore.upsert(docs)
    print("✅ Ads erfolgreich upserted.")
except Exception as e:
    print(f"❌ Fehler beim Upsert: {e}", file=sys.stderr)
    sys.exit(1)
