import requests
from django.conf import settings
from apps.integrations.models import MetaIntegration

def list_meta_campaigns(user):
    """
    Listet alle Facebook-/Instagram-Kampagnen des Users.
    """
    mi = MetaIntegration.objects.get(user=user)
    url = f"https://graph.facebook.com/v17.0/act_{mi.account_id}/campaigns"
    params = {
        "access_token": mi.access_token,
        "fields":       "id,name,status",
        "limit":        50,
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json().get("data", [])
    # Normiere die Rückgabe auf id, name, status
    campaigns = []
    for c in data:
        campaigns.append({
            "id":     c.get("id"),
            "name":   c.get("name"),
            "status": c.get("status"),
        })
    return campaigns
