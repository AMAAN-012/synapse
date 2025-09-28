# profiles/signals.py

from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Activity
from fitness.models import Workout # Assuming this model exists in your fitness app

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Workout)
def create_workout_activity(sender, instance, created, **kwargs):
    if created:
        Activity.objects.create(
            user=instance.user,
            content=f"logged a new workout: {instance.exercise_name}"
        )

# CORRECTED: This signal now correctly listens to changes on the 'follows' relationship.
@receiver(m2m_changed, sender=Profile.follows.through)
def create_follow_activity(sender, instance, action, pk_set, **kwargs):
    # 'instance' here is the Profile of the person who is doing the following
    if action == "post_add":
        followed_user_pk = list(pk_set)[0]
        # The pk_set gives the primary key of the Profile being followed
        followed_profile = Profile.objects.get(pk=followed_user_pk)
        Activity.objects.create(
            user=instance.user,
            content=f"started following {followed_profile.user.username}"
        )