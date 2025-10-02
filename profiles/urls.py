
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('users/', views.user_list_view, name='user_list'),
    path('feed/', views.activity_feed, name='activity_feed'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/toggle_follow/', views.toggle_follow_view, name='toggle_follow'),
    path('<str:username>/', views.profile_view, name='profile_view'), 
]