from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Activity
from fitness.models import Workout

@receiver(post_save, sender=User)
# Add 'raw' to the function arguments
def create_profile(sender, instance, created, raw, **kwargs):
    """
    Creates a profile for a new user, but NOT when loading data from a fixture.
    """
    # The 'raw' flag is True when loading data from a file (like loaddata).
    # This 'if not raw' check prevents the signal from running during data migration.
    if created and not raw:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Saves the profile whenever the user object is saved.
    """
    # This check prevents an error when a user is created for the first time,
    # ensuring the profile exists before trying to save it.
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Workout)
def create_workout_activity(sender, instance, created, **kwargs):
    """
    Creates an activity log when a new workout is saved.
    """
    if created:
        Activity.objects.create(
            user=instance.user,
            content=f"logged a new workout: {instance.exercise_name}"
        )

@receiver(m2m_changed, sender=Profile.follows.through)
def create_follow_activity(sender, instance, action, pk_set, **kwargs):
    """
    Creates an activity log when a user follows another user.
    """
    # 'instance' here is the Profile of the person who is doing the following
    if action == "post_add":
        followed_user_pk = list(pk_set)[0]
        followed_profile = Profile.objects.get(pk=followed_user_pk)
        Activity.objects.create(
            user=instance.user,
            content=f"started following {followed_profile.user.username}"
        )