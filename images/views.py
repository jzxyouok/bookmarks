from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from common.decorators import ajax_required
from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

import redis

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.uploader = request.user
            new_item.save()
            messages.success(request, 'Image added successfully.')
            create_action(request.user, 'bookmarked image', new_item)
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image:ranking', 1, image.id)
    return render(request, 'images/image/detail.html', {'section': 'images', 'image': image, 'total_views': total_views})


@ajax_required
@login_required
@require_POST
def image_favor(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'favor':
                image.favorited_by.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.favorited_by.remove(request.user)
        except Exception:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def image_list(request):
    object_list = Image.objects.all()
    paginator = Paginator(object_list, settings.IMAGES_PER_PAGE)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # stop the ajax
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    image_ranking = r.zrange('image:ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed_images = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed_images.sort(key=lambda x:image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'section': 'images', 'most_viewed_images': most_viewed_images})
