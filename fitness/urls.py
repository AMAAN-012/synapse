from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    # URL for the workout list (e.g., /fitness/)
    path('', views.workout_list, name='workout_list'),
    
    # URL for adding a new workout (e.g., /fitness/add/)
    path('add/', views.add_workout, name='add_workout'),

     path('progress/', views.progress_view, name='progress_view'),
]