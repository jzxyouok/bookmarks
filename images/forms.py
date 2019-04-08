import requests
from urllib.request import urlopen
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput,}

    def clean_url(self):
        url = self.cleaned_data['url']
        allowed_exts = ['jpg', 'jpeg', 'png']
        if not any(ext in url for ext in allowed_exts):
            raise forms.ValidationError(f"Sorry, supported extensions are {', '.join(allowed_exts)}")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        url = self.cleaned_data['url']
        ext = url.rsplit('.', 1)[1].lower()
        image_name = f'{slugify(image.title)}.{ext}'
        content = requests.get(url).content
        image.image.save(image_name, ContentFile(content), save=False)
        if commit:
            image.save()
        return image
