# profiles/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, help_text="A little bit about yourself.")
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )


    def __str__(self):
        return f'{self.user.username} Profile'

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Activities" 

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'