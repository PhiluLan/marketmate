import datetime
from django.conf import settings
from google.ads.googleads.client import GoogleAdsClient
from apps.integrations.models import Integration

def _get_client(user):
    integ = Integration.objects.get(user=user, provider="google")
    config = {
        "developer_token": settings.GOOGLE_ADS_DEVELOPER_TOKEN,
        "refresh_token":   integ.refresh_token,
        "client_id":       settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret":   settings.GOOGLE_OAUTH_CLIENT_SECRET,
    }
    return GoogleAdsClient.load_from_dict(config)

def list_campaigns(user):
    integ = Integration.objects.filter(user=user, provider="google").first()
    if not integ or not integ.account_id:
        print("🔍 list_campaigns: no integration or account_id for user", user)
        return []

    customer_id = integ.account_id.replace('-', '')
    print("🔍 list_campaigns: using customer_id =", customer_id)

    client = GoogleAdsClient.load_from_dict({
        "developer_token":   settings.GOOGLE_ADS_DEVELOPER_TOKEN,
        "refresh_token":     integ.refresh_token,
        "client_id":         settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret":     settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "login_customer_id": customer_id,
        "use_proto_plus":    True,
    })
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status
        FROM campaign
        ORDER BY campaign.id
    """
    print("🔍 list_campaigns: running query")

    # Use search() for simplicity
    response = ga_service.search(customer_id=customer_id, query=query)

    campaigns = []
    for row in response:
        campaigns.append({
            "id":     row.campaign.id,
            "name":   row.campaign.name,
            "status": row.campaign.status.name,
        })

    print("🔍 list_campaigns: found campaigns:", campaigns)
    return campaigns


def list_accessible_customers(refresh_token):
    """
    Ruft alle Google Ads-Kunden auf, zu denen dieses Token Zugriff hat.
    """
    config = {
        "developer_token":   settings.GOOGLE_ADS_DEVELOPER_TOKEN,
        "refresh_token":     refresh_token,
        "client_id":         settings.GOOGLE_OAUTH_CLIENT_ID,
        "client_secret":     settings.GOOGLE_OAUTH_CLIENT_SECRET,
        "use_proto_plus":    True,
    }
    client = GoogleAdsClient.load_from_dict(config)
    service = client.get_service("CustomerService")
    response = service.list_accessible_customers()
    # resource_names sind wie ["customers/1234567890", "customers/2744473809", ...]
    ids = [rn.split("/")[1] for rn in response.resource_names]
    return ids
