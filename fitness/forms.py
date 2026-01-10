from django import forms
from .models import Workout
from .models import BodyMeasurement

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise_name', 'sets', 'reps', 'weight_kg']


class BodyMeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = ['weight', 'chest', 'waist', 'biceps']
        
        # Tailwind Styling widgets ke through inject kar rahe hain
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500', 'placeholder': 'Ex: 75.5'}),
            'chest': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500', 'placeholder': 'Optional'}),
            'waist': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500', 'placeholder': 'Optional'}),
            'biceps': forms.NumberInput(attrs={'class': 'w-full bg-slate-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-purple-500', 'placeholder': 'Optional'}),
        }       