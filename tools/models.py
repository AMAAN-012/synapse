from django.db import models
from django.contrib.auth.models import User
import uuid

class AdvancedNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Extra features
    tags = models.CharField(max_length=200, blank=True)
    is_favorite = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    audio_recording = models.FileField(upload_to='notes_audio/', blank=True, null=True)
    shareable_link = models.URLField(blank=True, null=True)
    checklist = models.JSONField(default=list, blank=True) 
    
    def generate_share_link(self):
        token = uuid.uuid4()
        self.shareable_link = f"https://yourdomain.com/share/{token}/"
        self.save()
        return self.shareable_link

    def __str__(self):
        return self.title


class NoteHistory(models.Model):
    note = models.ForeignKey(AdvancedNote, on_delete=models.CASCADE, related_name='history')
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text[:50]}..." by {self.author}'
    
    
class QuoteVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])
    
    class Meta:
        unique_together = ('user', 'quote')
    
    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on quote {self.quote.pk}"