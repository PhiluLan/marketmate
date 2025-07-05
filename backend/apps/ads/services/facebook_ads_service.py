import json
import requests
from django.conf import settings

# ─── Mapping alter → neuer Objective-Werte ─────────────────────────
OBJECTIVE_MAP = {
    "WEBSITE_CONVERSIONS": "OUTCOME_TRAFFIC",
    "LINK_CLICKS":          "OUTCOME_TRAFFIC",
    "TRAFFIC":              "OUTCOME_TRAFFIC",
    "AWARENESS":            "OUTCOME_AWARENESS",
    "BRAND_AWARENESS":      "OUTCOME_AWARENESS",
    "CONVERSIONS":          "OUTCOME_SALES",
    "LEAD_GENERATION":      "OUTCOME_LEADS",
    "VIDEO_VIEWS":          "OUTCOME_ENGAGEMENT",
    "ENGAGEMENT":           "OUTCOME_ENGAGEMENT",
    "APP_INSTALLS":         "OUTCOME_APP_PROMOTION",
}

BASE = "https://graph.facebook.com/v17.0"

def create_meta_ad_campaign(
    account_id: str,
    campaign_name: str,
    objective: str,
    daily_budget: int,
    status: str                   = "PAUSED",
    spend_cap: int | None         = None,
    start_time: str | None       = None,
    end_time: str | None         = None,
    special_ad_categories: str    = "NONE",
    buying_type: str              = "AUCTION",
    attribution_spec: list | None = None
) -> dict:
    """
    Legt eine neue Meta-Ads-Kampagne an.
    Alte Objectives werden automatisch auf die neuen OUTCOME_*-Werte gemappt.
    """
    # 1) Objective in gültigen Outcome-Wert übersetzen
    objective = OBJECTIVE_MAP.get(objective.upper(), objective)

    # 2) API-Endpunkt
    url = f"{BASE}/act_{account_id}/campaigns"

    # 3) Payload zusammenstellen
    data: dict = {
        "access_token":          settings.FB_SYSTEM_TOKEN,
        "name":                  campaign_name,
        "objective":             objective,
        "daily_budget":          daily_budget,
        "status":                status,
        "special_ad_categories": special_ad_categories,
        "buying_type":           buying_type,
    }
    if spend_cap is not None:
        data["spend_cap"] = spend_cap
    if start_time:
        data["start_time"] = start_time
    if end_time:
        data["end_time"] = end_time
    if attribution_spec is not None:
        # Meta erwartet JSON als String
        data["attribution_spec"] = json.dumps(attribution_spec)

    # 4) Request ausführen
    res = requests.post(url, data=data)
    if res.status_code != 200:
        # Bei Fehlern komplette Antwort ausgeben
        raise RuntimeError(f"Meta-API-Error {res.status_code}: {res.text}")

    # 5) Erfolgsantwort zurückgeben
    return res.json()
