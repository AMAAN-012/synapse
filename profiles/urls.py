# profiles/urls.py

from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # New URL for the community page
    path('users/', views.user_list_view, name='user_list'),
    
    # Existing URLs
    path('feed/', views.activity_feed, name='activity_feed'),
    path('edit/', views.edit_profile, name='edit_profile'),
    
    # New URL for a single button follow/unfollow
    path('<str:username>/toggle_follow/', views.toggle_follow_view, name='toggle_follow'),
    
    # Keep this at the bottom as it's a general pattern
    path('<str:username>/', views.profile_view, name='profile_view'), 
]