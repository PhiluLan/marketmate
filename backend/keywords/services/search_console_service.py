# backend/keywords/services/search_console_service.py

import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

def _get_searchconsole_client():
    """
    Erzeugt erst bei Bedarf den GSC-Client.
    Liest SERVICE_ACCOUNT_FILE und SITE_URL aus ENV und wirft
    eine RuntimeError, falls etwas fehlt.
    """
    service_account_file = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    site_url             = os.getenv("GSC_SITE_URL")

    if not service_account_file or not os.path.isfile(service_account_file):
        raise RuntimeError(f"GSC service account file not found: {service_account_file!r}")
    if not site_url:
        raise RuntimeError("GSC_SITE_URL ist nicht gesetzt")

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    client = build("searchconsole", "v1", credentials=creds)
    return client, site_url


def fetch_rankings_for_domain(
    keywords: list[str],
    days_back: int = 7
) -> list[dict]:
    """
    Ruft für jedes Keyword die durchschnittliche Position,
    Impressionen und Klicks der letzten `days_back` Tage ab.
    """
    client, site_url = _get_searchconsole_client()

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days_back)

    body = {
        "startDate": start_date.isoformat(),
        "endDate":   end_date.isoformat(),
        "dimensions": ["query"],
        "dimensionFilterGroups": [{
            "filters": [
                {"dimension": "query", "expression": kw}
                for kw in keywords
            ]
        }],
        "rowLimit": len(keywords),
    }

    resp = (
        client
        .searchanalytics()
        .query(siteUrl=site_url, body=body)
        .execute()
    )

    results = []
    for row in resp.get("rows", []):
        results.append({
            "keyword":     row["keys"][0],
            "position":    row.get("position"),
            "impressions": row.get("impressions"),
            "clicks":      row.get("clicks"),
            "source":      "GSC",
        })
    return results
