from django.urls import path

from .views import image_create, image_detail, image_favor, image_list, image_ranking

app_name = 'images'

urlpatterns = [
    path('create/', image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', image_detail, name='detail'),
    path('favor/', image_favor, name='favor'),
    path('ranking/', image_ranking, name='ranking'),
    path('', image_list, name='list'),
]
