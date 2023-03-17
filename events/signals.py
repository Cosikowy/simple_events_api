from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from events.models import Event, Performence


@receiver(pre_save, sender=Performence)
def check_performences(sender, instance, **kwargs):
    ...
