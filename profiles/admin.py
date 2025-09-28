# profiles/admin.py

from django.contrib import admin
from .models import Profile, Activity # Import Activity

admin.site.register(Profile)
admin.site.register(Activity) # Register Activity model