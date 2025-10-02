from django.contrib import admin
from .models import AdvancedNote, NoteHistory, Quote,QuoteVote

@admin.register(AdvancedNote)
class AdvancedNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_favorite', 'created_at', 'updated_at')
    list_filter = ('user', 'is_favorite', 'created_at')
    search_fields = ('title', 'content', 'tags')
    raw_id_fields = ('user',)

@admin.register(NoteHistory)
class NoteHistoryAdmin(admin.ModelAdmin):

    list_display = ('note', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('note__title',)
    raw_id_fields = ('note',)
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'is_approved', 'created_by', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('text', 'author')
    list_editable = ('is_approved',)
   
admin.site.register(QuoteVote)