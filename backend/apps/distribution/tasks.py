from celery import shared_task
import sys
from .models import ScheduledPost

# Ads-Service
from apps.ads.services.facebook_ads_service import create_meta_ad_campaign
# organische Post-Services (nun vorhanden)
from .services.facebook_post_service import send_to_facebook
from .services.instagram_post_service import send_to_instagram
from .services.email_service import send_email

@shared_task
def send_scheduled_post(scheduled_post_id):
    post = ScheduledPost.objects.get(id=scheduled_post_id)
    try:
        if post.channel == "facebook_ads":
            create_meta_ad_campaign(
                account_id       = post.content.ad_account_id,
                campaign_name    = post.content.title,
                objective        = post.content.objective,
                daily_budget     = post.content.daily_budget,
                status           = "PAUSED",
                spend_cap        = getattr(post.content, "spend_cap", None),
                start_time       = post.scheduled_time.isoformat(),
                end_time         = getattr(post.content, "end_time", None)
                                      and post.content.end_time.isoformat(),
                attribution_spec = getattr(post.content, "attribution_spec", None),
            )
        elif post.channel == "facebook":
            send_to_facebook(post.content)
        elif post.channel == "instagram":
            send_to_instagram(post.content)
        elif post.channel == "email":
            send_email(post.content)

        post.status = "sent"
    except Exception as e:
        print(f"❌ Fehler bei ScheduledPost {post.id}: {e}", file=sys.stderr)
        post.status = "failed"
    post.save()
