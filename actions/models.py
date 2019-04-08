from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'actions', db_index=True)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType, models.CASCADE, 'target_obj', blank=True, null=True)
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)