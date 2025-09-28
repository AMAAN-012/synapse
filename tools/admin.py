from django.contrib import admin
from .models import AdvancedNote, NoteHistory, Quote,QuoteVote

@admin.register(AdvancedNote)
class AdvancedNoteAdmin(admin.ModelAdmin):
    # Customize the way AdvancedNote objects are displayed in the admin list view
    list_display = ('title', 'user', 'is_favorite', 'created_at', 'updated_at')
    
    # Add filters to easily sort notes by user, favorite status, and creation date
    list_filter = ('user', 'is_favorite', 'created_at')
    
    # Add a search bar to find notes by title, content, or tags
    search_fields = ('title', 'content', 'tags')
    
    # Use a raw ID field for the user to improve performance with many users
    raw_id_fields = ('user',)

@admin.register(NoteHistory)
class NoteHistoryAdmin(admin.ModelAdmin):
    # Customize the display for NoteHistory
    list_display = ('note', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('note__title',)
    raw_id_fields = ('note',)

# Register the Quote model
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('text', 'author')
    list_editable = ('is_approved',)
   
admin.site.register(QuoteVote)