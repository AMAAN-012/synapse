# profiles/admin.py

from django.contrib import admin
from .models import Profile, Activity 

admin.site.register(Profile)
admin.site.register(Activity)