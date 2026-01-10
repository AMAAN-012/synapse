from django.db import models
from django.contrib.auth.models import User
from datetime import date
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight_kg = models.FloatField(blank=True, null=True, help_text="Weight in kilograms")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.exercise_name} on {self.date}"
    
class BodyMeasurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) # Jis din entry ki, wahi date automatically aa jayegi
    weight = models.FloatField(help_text="Weight in KG")
    
    # Optional fields (User chaho toh bhare, warna khali chode)
    chest = models.FloatField(null=True, blank=True, help_text="in inches")
    waist = models.FloatField(null=True, blank=True, help_text="in inches")
    biceps = models.FloatField(null=True, blank=True, help_text="in inches")

    def __str__(self):
        return f"{self.user.username} - {self.weight}kg on {self.date}"

    class Meta:
        ordering = ['-date']   