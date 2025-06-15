#!/usr/bin/env python3
"""
Script zum Anlegen eines Google Ads Sandbox-Accounts
unter deinem Manager-Konto via API.
"""
import os
import sys
import tempfile
from pathlib import Path
from string import Template
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient

# 1) .env laden
here = Path(__file__).parent
load_dotenv(dotenv_path=here / ".env")

def load_google_ads_client() -> GoogleAdsClient:
    # Platzhalter in google-ads.yaml mit echten Env-Werten füllen
    raw = (here / "google-ads.yaml").read_text()
    filled = Template(raw).substitute(os.environ)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    tmp.write(filled.encode("utf-8"))
    tmp.flush(); tmp.close()
    return GoogleAdsClient.load_from_storage(path=tmp.name)

def create_sandbox_client(manager_customer_id: str) -> str:
    client = load_google_ads_client()
    # sicherstellen, dass der Header stimmt
    client.login_customer_id = manager_customer_id

    svc = client.get_service("CustomerService")

    # Dict-API mit 'customer_client', nicht 'operation'
    req = {
        "customer_id": manager_customer_id,
        "customer_client": {
            "descriptive_name": "MarketMate API Sandbox",
            "currency_code":     "EUR",
            "time_zone":         "Europe/Zurich"
        }
    }

    resp = svc.create_customer_client(request=req)
    return resp.resource_name.split("/")[-1]

def main():
    mgr = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID") or input(
        "Manager-Customer-ID (10 Ziffern): "
    ).strip()
    if not (mgr.isdigit() and len(mgr) == 10):
        print("❌ Manager-ID muss 10 Ziffern haben."); sys.exit(1)

    try:
        new_cid = create_sandbox_client(mgr)
        print(f"✅ Neuer Test-Account angelegt: Customer ID = {new_cid}")
    except Exception as e:
        print("❌ Fehler beim Anlegen des Sandbox-Accounts:"); print(e); sys.exit(1)

if __name__ == "__main__":
    main()
