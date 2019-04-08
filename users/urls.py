from django.urls import path

from .views import SignUpView, dashboard, EditView, user_list, user_detail, user_follow

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', dashboard, name='dashboard'),
    path('<int:pk>/edit/', EditView.as_view(), name='edit'),
    path('all/', user_list, name='user_list'),
    path('follow/', user_follow, name='user_follow'),
    path('<username>/', user_detail, name='user_detail')
]
