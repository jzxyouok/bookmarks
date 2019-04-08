from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy


# Create your models here.
class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'rel_from_set')
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, 'rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class CustomUser(AbstractUser):
    birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)

    def get_absolute_url(self):
        return reverse_lazy("user_detail", kwargs={"username": self.username})
