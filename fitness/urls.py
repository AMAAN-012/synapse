from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
   
    path('', views.workout_list, name='workout_list'),
    path('add/', views.add_workout, name='add_workout'),
    path('progress/', views.progress_view, name='progress_view'),
]