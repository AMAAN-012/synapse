from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WorkoutForm
from .models import Workout
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Coalesce
from collections import defaultdict
from datetime import date, timedelta
import json

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
    workouts = Workout.objects.filter(user=request.user).order_by('date')
    
    daily_volumes = defaultdict(float)
    for workout in workouts:
        volume = (workout.sets or 0) * (workout.reps or 0) * (workout.weight_kg or 0)
        daily_volumes[workout.date.strftime('%b %d')] += volume

    line_chart_labels = list(daily_volumes.keys())
    line_chart_data = list(daily_volumes.values())
    
    exercise_data = Workout.objects.filter(user=request.user)\
        .values('exercise_name')\
        .annotate(
            total_volume=Sum(
                F('sets') * F('reps') * Coalesce(F('weight_kg'), Value(0)),
                # 👇 2. ADD THIS output_field ARGUMENT
                output_field=FloatField()
            )
        )\
        .order_by('-total_volume')

    doughnut_labels = [item['exercise_name'] for item in exercise_data]
    doughnut_data = [item['total_volume'] for item in exercise_data]

    context = {
        'line_labels': json.dumps(line_chart_labels),
        'line_data': json.dumps(line_chart_data),
        'doughnut_labels': json.dumps(doughnut_labels),
        'doughnut_data': json.dumps(doughnut_data),
    }

    return render(request, 'fitness/progress_view.html', context)