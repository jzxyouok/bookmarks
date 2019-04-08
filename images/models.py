from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=360)
    slug = models.SlugField(max_length=360, blank=True)
    url = models.URLField(max_length=360)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uploaded_images', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorites', blank=True)
    total_favors = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])
    