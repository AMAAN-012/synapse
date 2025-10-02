from django.db import models
from django.contrib.auth.models import User
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight_kg = models.FloatField(blank=True, null=True, help_text="Weight in kilograms")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.exercise_name} on {self.date}"