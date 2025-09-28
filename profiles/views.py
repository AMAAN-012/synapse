# profiles/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from datetime import date, timedelta 
from .models import Profile, Activity
from .forms import ProfileForm
from fitness.models import Workout # Make sure to import your Workout model

# NEW VIEW: For the community/users page
@login_required
def user_list_view(request):
    users = User.objects.exclude(pk=request.user.pk)
    
    # Get profiles that the current user is following
    following_profiles = request.user.profile.follows.all()
    # Get the user objects from those profiles for easy checking in template
    following_list = User.objects.filter(profile__in=following_profiles)

    context = {
        'users': users,
        'following_list': following_list
    }
    return render(request, 'profiles/user_list.html', context)


# UPDATED VIEW: Now sends all the data the template needs
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    is_following = request.user.profile.follows.filter(pk=profile.pk).exists()
    
    # --- DATA FOR THE PROFILE TEMPLATE ---
    workouts = Workout.objects.filter(user=profile_user).order_by('-date')
    recent_workouts = workouts[:5]
    total_workouts = workouts.count()

    following_count = profile.follows.count()
    followers_count = profile.followed_by.count()

    # --- REAL STREAK CALCULATION LOGIC (from your fitness app) ---
    streak_count = 0
    today = date.today()
    workout_dates = sorted(list(set(workouts.values_list('date', flat=True))), reverse=True)

    if workout_dates:
        # Check if last workout was today or yesterday
        if workout_dates[0] == today or workout_dates[0] == today - timedelta(days=1):
            streak_count = 1
            for i in range(len(workout_dates) - 1):
                if workout_dates[i] - timedelta(days=1) == workout_dates[i+1]:
                    streak_count += 1
                else:
                    break
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_following': is_following,
        'workouts': recent_workouts,
        'total_workouts': total_workouts,
        'following_count': following_count,
        'followers_count': followers_count,
        'streak_count': streak_count, # Ab yeh aalokik hai!
    }
    return render(request, 'profiles/profile_detail.html', context)

# NEW VIEW: To handle both follow and unfollow with one button
@login_required
@require_POST # Ensures this view only accepts POST requests
def toggle_follow_view(request, username):
    user_to_toggle = get_object_or_404(User, username=username)
    profile_to_toggle = user_to_toggle.profile
    current_user_profile = request.user.profile

    # Check if the user is currently being followed
    if profile_to_toggle in current_user_profile.follows.all():
        # If yes, unfollow
        current_user_profile.follows.remove(profile_to_toggle)
    else:
        # If no, follow
        current_user_profile.follows.add(profile_to_toggle)
        
    # Redirect back to the user's profile page
    return redirect('profiles:profile_view', username=username)


# This view is okay, no changes needed
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            Activity.objects.create(user=request.user, content="Updated their profile.")
            return redirect('profiles:profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})


# This view is also okay, no changes needed
@login_required
def activity_feed(request):
    followed_profiles = request.user.profile.follows.all()
    activities = Activity.objects.filter(user__profile__in=followed_profiles).order_by('-timestamp')
    context = {'activities': activities}
    return render(request, 'profiles/activity_feed.html', context)