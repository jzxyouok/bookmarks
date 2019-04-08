from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Contact
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


class SignUpView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = "Welcome, %(username)s!"


class EditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'user/edit.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('dashboard')
    success_message = "Profile updated successfully"


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]
    return render(request, 'user/dashboard.html', {'section': 'dashboard', 'actions': actions})


@login_required
def user_list(request):
    users = CustomUser.objects.filter(is_active=True)
    return render(request, 'user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username, is_active=True)
    return render(request, 'user/detail.html', {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = CustomUser.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
