#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Service zur Abfrage von Keyword-Ideen-Metriken (Suchvolumen, Wettbewerb, CPC)
über die Google Ads API.
"""

import os
import tempfile
from pathlib import Path
from string import Template

from django.conf import settings
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from dotenv import load_dotenv

# ─── 1) Lade .env (damit ${…}-Platzhalter in google-ads.yaml funktionieren) ───
load_dotenv(dotenv_path=Path(settings.BASE_DIR) / ".env")


# ─── 2) Hilfsfunktionen, um google-ads.yaml mit Env-Werten zu füllen ───
def _find_and_fill_yaml() -> Path:
    orig = Path(settings.BASE_DIR) / "google-ads.yaml"
    if not orig.exists():
        raise FileNotFoundError(f"Config nicht gefunden: {orig}")
    raw = orig.read_text(encoding="utf-8")
    try:
        filled = Template(raw).substitute(os.environ)
    except KeyError as e:
        raise RuntimeError(f"Env-Var fehlt für YAML-Platzhalter: {e}")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".yaml")
    tmp.write(filled.encode("utf-8"))
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def _load_client() -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(path=str(_find_and_fill_yaml()))


# ─── 3) Mapping für Competition-Level, falls kein .name verfügbar ───
_COMP_LEVEL = {
    0: "UNSPECIFIED",
    1: "UNKNOWN",
    2: "LOW",
    3: "MEDIUM",
    4: "HIGH",
}


def fetch_keyword_ideas(
    keywords: list[str],
    client_customer_id: str,
    language_id: int = 1000,
    region: str | None = None
) -> list[dict]:
    """
    Liefert für eine Liste von Keywords:
      - monthly_searches (int)
      - competition       (str: LOW, MEDIUM, HIGH)
      - low_cpc           (float, EUR)
      - high_cpc          (float, EUR)

    :param keywords:             Liste von Suchbegriffen (Seed-Keywords)
    :param client_customer_id:   Die zu analysierende Kunden-ID (Google Ads)
    :param language_id:          Optional: Language Constant ID (Default 1000 = englisch)
    :param region:               Optional: ISO-Ländercode (z.B. "CH") für Geo-Targeting
    :raises RuntimeError:        Wenn Env-Var fehlt oder Geo-Target nicht gefunden
    """
    # 1) Client laden und Login-Header setzen
    client = _load_client()
    manager_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    if not (manager_id and manager_id.isdigit() and len(manager_id) == 10):
        raise RuntimeError("GOOGLE_ADS_LOGIN_CUSTOMER_ID in .env fehlt oder ist ungültig")
    client.login_customer_id = manager_id

    # 2) Services holen
    idea_svc = client.get_service("KeywordPlanIdeaService")
    ga_svc   = client.get_service("GoogleAdsService")

    # 3) Resource-Namen für Sprache
    language_rn = ga_svc.language_constant_path(language_id)

    # 4) Geo-Target bestimmen
    if region:
        # Suche Geo-Target über country_code
        query = (
            f"SELECT geo_target_constant.resource_name "
            f"FROM geo_target_constant "
            f"WHERE geo_target_constant.country_code = '{region.upper()}' "
            "LIMIT 1"
        )
        try:
            resp = ga_svc.search(customer_id=client_customer_id, query=query)
            geo_rns = [row.geo_target_constant.resource_name for row in resp]
        except GoogleAdsException as ex:
            raise RuntimeError(f"Fehler bei Geo-Target-Suche: {ex}") from ex

        if not geo_rns:
            raise RuntimeError(f"Kein Geo-Target gefunden für Region '{region}'")
    else:
        # Fallback: Schweiz (ID 1023191)
        geo_rns = [ga_svc.geo_target_constant_path("1023191")]

    # 5) Request als Dict bauen
    request = {
        "customer_id": client_customer_id,
        "keyword_seed": {"keywords": keywords},
        "language": language_rn,
        "geo_target_constants": geo_rns,
        "keyword_plan_network": client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH_AND_PARTNERS
    }

    # 6) API aufrufen
    try:
        response = idea_svc.generate_keyword_ideas(request=request)
    except GoogleAdsException as ex:
        raise RuntimeError(f"Google Ads Fehler: {ex}") from ex

    # 7) Antwort parsen
    results: list[dict] = []
    for idea in response:
        m = idea.keyword_idea_metrics

        # Competition ggf. aus Enum-Mapping holen
        comp_val = m.competition
        if hasattr(comp_val, "name"):
            comp_str = comp_val.name
        else:
            comp_str = _COMP_LEVEL.get(comp_val, str(comp_val))

        results.append({
            "keyword":          idea.text,
            "monthly_searches": m.avg_monthly_searches,
            "competition":      comp_str,
            "low_cpc":          m.low_top_of_page_bid_micros / 1e6,
            "high_cpc":         m.high_top_of_page_bid_micros / 1e6,
        })

    return results
