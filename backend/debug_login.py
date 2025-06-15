#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1) .env laden
here = Path(__file__).parent
load_dotenv(dotenv_path=here / ".env")

# 2) Env-Var ausgeben
login_env = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
print(f"ENV → GOOGLE_ADS_LOGIN_CUSTOMER_ID = {login_env!r}")

# 3) Google-Ads-Client laden und YAML-Wert ausgeben
from google.ads.googleads.client import GoogleAdsClient
client = GoogleAdsClient.load_from_storage(path=str(here / "google-ads.yaml"))
yaml_login = client._configuration.login_customer_id
print(f"YAML → login_customer_id      = {yaml_login!r}")

sys.exit(0)
