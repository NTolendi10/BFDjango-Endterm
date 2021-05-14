from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Gadget
import logging
logger = logging.getLogger('api')


@receiver(post_delete, sender=Gadget)
def product_removed(sender, instance, using, **kwargs):
    instance.is_active = False
    instance.save()
    logger.info(f"{instance} removed from active")
