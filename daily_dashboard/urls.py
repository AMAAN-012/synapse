# daily_dashboard/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App URLs
    path('tools/notes/', include('tools.urls', namespace='notes')),
    # CORRECTED: Added the required namespace for the fitness app
    path('fitness/', include('fitness.urls', namespace='fitness')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    
    # Homepage URL
    path('', views.daily_dashboard_index, name='daily_dashboard_index'),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),

    path('permission-denied/', views.permission_denied, name='permission_denied'),
]

# CORRECTED: Fixed the indentation and removed the extra 'if' statement.
# This block will serve both static files (like your video) and media files (user uploads).
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)