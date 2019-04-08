from django.contrib import admin

from .models import Image
# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', 'total_favors']
    list_filter = ['created']
