from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ScheduledPost
from .tasks import send_scheduled_post

@receiver(post_save, sender=ScheduledPost)
def schedule_task(sender, instance, created, **kwargs):
    if created and instance.status == "pending":
        send_scheduled_post.apply_async(
            args=[instance.id],
            eta=instance.scheduled_time
        )
