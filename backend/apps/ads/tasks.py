# apps/ads/tasks.py
from celery import shared_task
import requests, os, sys
from dotenv import load_dotenv
from services.vector_store import VectorStore
from apps.integrations.models import MetaIntegration

@shared_task
def fetch_all_fb_ads():
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
    integrations = MetaIntegration.objects.all()
    for mi in integrations:
        token = mi.access_token.strip()
        account = mi.account_id
        url = f"https://graph.facebook.com/v17.0/act_{account}/ads"
        params = {
            "access_token": token,
            "fields": "id,name,insights.limit(1){impressions,clicks,spend}",
            "limit": 50
        }
        r = requests.get(url, params=params)
        if r.status_code != 200:
            print(f"❌ Facebook Error for user {mi.user}: {r.text}", file=sys.stderr)
            continue
        ads = r.json().get("data", [])
        docs = []
        for ad in ads:
            ins = ad.get("insights",{}).get("data",[{}])[0]
            text = (
                f"User:{mi.user.id} | Ad-ID:{ad['id']} | "
                f"Name:{ad.get('name','–')} | "
                f"Impr:{ins.get('impressions','–')}, "
                f"Clicks:{ins.get('clicks','–')}, "
                f"Spend:CHF{ins.get('spend','–')}"
            )
            docs.append({"id":f"{mi.user.id}-fbad-{ad['id']}", "text":text})
        if docs:
            print(f"Upserting {len(docs)} Ads for user {mi.user.username}…")
            VectorStore.upsert(docs)
