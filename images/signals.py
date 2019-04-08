from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

@receiver(m2m_changed, sender=Image.favorited_by.through)
def favorited_by_changed(sender, instance, **kwargs):
    instance.total_favors = instance.favorited_by.count()
    instance.save()
