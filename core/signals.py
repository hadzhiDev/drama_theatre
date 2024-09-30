from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from core.models import *


@receiver(pre_delete, sender=HallRow)
def delete_seats_and_empty_spots(sender, instance=HallRow, *args, **kwargs):
    for empty_space in instance.empty_spaces.all():
        empty_space.delete()
