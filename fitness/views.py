from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# 👇 Updated Imports: Added BodyMeasurementForm and BodyMeasurement model
from .forms import WorkoutForm, BodyMeasurementForm
from .models import Workout, BodyMeasurement
from django.db.models import Sum, F, Value, FloatField, Count, Max
from django.db.models.functions import Coalesce
from collections import defaultdict
from datetime import date, timedelta
import json

# ==========================================
# EXISTING VIEWS (No Changes Made)
# ==========================================

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    streak_count = 0
    today = date.today()
    
    workout_dates = sorted(list(set(workouts.values_list('date', flat=True))), reverse=True)

    if workout_dates:
        if workout_dates[0] == today or workout_dates[0] == today - timedelta(days=1):
            streak_count = 1
            for i in range(len(workout_dates) - 1):
                if workout_dates[i] - timedelta(days=1) == workout_dates[i+1]:
                    streak_count += 1
                else:
                    break

    context = {
        'workouts': workouts,
        'streak_count': streak_count,
    }
    return render(request, 'fitness/workout_list.html', context)

@login_required
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('fitness:workout_list')
    else:
        form = WorkoutForm()
    
    return render(request, 'fitness/add_workout.html', {'form': form})

@login_required
def progress_view(request):
    # ---------------------------------------------------------
    # LOGIC 1: STRENGTH TREND (Line Chart)
    # ---------------------------------------------------------
    strength_workouts = Workout.objects.filter(
        user=request.user, 
        weight_kg__gt=0
    ).order_by('date')
    
    strength_progress = defaultdict(float)
    
    for workout in strength_workouts:
        # Calculate Est. 1 Rep Max
        one_rm = workout.weight_kg * (1 + (workout.reps / 30))
        date_str = workout.date.strftime('%b %d')
        
        if one_rm > strength_progress[date_str]:
            strength_progress[date_str] = round(one_rm, 2)

    line_chart_labels = list(strength_progress.keys())
    line_chart_data = list(strength_progress.values())
    
    # ---------------------------------------------------------
    # LOGIC 2: EXERCISE FREQUENCY (Doughnut Chart)
    # ---------------------------------------------------------
    exercise_data = Workout.objects.filter(user=request.user)\
        .values('exercise_name')\
        .annotate(total_count=Count('id'))\
        .order_by('-total_count')[:5]

    doughnut_labels = [item['exercise_name'] for item in exercise_data]
    doughnut_data = [item['total_count'] for item in exercise_data]

    context = {
        'line_labels': json.dumps(line_chart_labels),
        'line_data': json.dumps(line_chart_data),
        'doughnut_labels': json.dumps(doughnut_labels),
        'doughnut_data': json.dumps(doughnut_data),
    }

    return render(request, 'fitness/progress_view.html', context)


# ==========================================
# NEW VIEW ADDED BELOW
# ==========================================

@login_required
def measurements_view(request):
    """
    Handles displaying the history of body measurements
    and saving new measurement entries.
    """
    # 1. Logic to save new data (POST request)
    if request.method == 'POST':
        form = BodyMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user  # Attach current user
            measurement.save()
            return redirect('fitness:measurements') # Redirect to same page (prevents resubmission)
    else:
        # GET request: Show empty form
        form = BodyMeasurementForm()

    # 2. Logic to fetch history (GET request)
    # Fetch data for this user only
    history = BodyMeasurement.objects.filter(user=request.user).order_by('-date')

    context = {
        'form': form,
        'history': history
    }
    
    return render(request, 'fitness/measurements.html', context)