from django.urls import path
from . import views 
# Set app name for namespacing
app_name = 'tools'

urlpatterns = [
    # Notes app URLs...
    path('notes/', views.NotesListView.as_view(), name='notes_list'),
    path('notes/create/', views.NotesCreateView.as_view(), name='notes_create'),
    path('notes/<int:pk>/', views.NotesDetailView.as_view(), name='notes_detail'),
    path('notes/<int:pk>/update/', views.NotesUpdateView.as_view(), name='notes_update'),
    path('notes/<int:pk>/delete/', views.NotesDeleteView.as_view(), name='notes_delete'),


    path('quotes/', views.quote_of_the_day, name='quote_of_the_day'),
    path('quotes/submit/', views.QuoteCreateView.as_view(), name='quote_submit'),
    path('quotes/<int:pk>/update/', views.QuoteUpdateView.as_view(), name='quote_update'),
    path('quotes/<int:pk>/delete/', views.QuoteDeleteView.as_view(), name='quote_delete'),
    path('quotes/vote/', views.vote_quote, name='quote_vote'),
]

