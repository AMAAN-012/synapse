from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Activity
from fitness.models import Workout

@receiver(post_save, sender=User)

def create_profile(sender, instance, created, raw, **kwargs):

    if created and not raw:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Workout)
def create_workout_activity(sender, instance, created, **kwargs):
   
    if created:
        Activity.objects.create(
            user=instance.user,
            content=f"logged a new workout: {instance.exercise_name}"
        )

@receiver(m2m_changed, sender=Profile.follows.through)
def create_follow_activity(sender, instance, action, pk_set, **kwargs):

    if action == "post_add":
        followed_user_pk = list(pk_set)[0]
        followed_profile = Profile.objects.get(pk=followed_user_pk)
        Activity.objects.create(
            user=instance.user,
            content=f"started following {followed_profile.user.username}"
        )