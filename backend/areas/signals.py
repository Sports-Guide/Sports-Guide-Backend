from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import ModerationStatus
from .models import Area
from .tasks import send_moderation_email


@receiver(post_save, sender=Area)
def send_moderation_status_email(instance, **kwargs):
    if instance.moderation_status == ModerationStatus.APPROVED.value:
        send_moderation_email(instance.author.email, 'approved')

    if instance.moderation_status == ModerationStatus.REJECTED.value:
        send_moderation_email(instance.author.email, 'rejected')
