from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise_name', 'sets', 'reps', 'weight_kg']