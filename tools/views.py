from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
import requests
from .models import AdvancedNote, NoteHistory, Quote, QuoteVote
from .forms import QuoteForm
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

class NotesListView(LoginRequiredMixin, ListView):
    model = AdvancedNote
    template_name = 'tools/notes/notes_list.html'
    context_object_name = 'notes_list'

    def get_queryset(self):
        return AdvancedNote.objects.filter(user=self.request.user).order_by('-created_at')


class NotesDetailView(LoginRequiredMixin, DetailView):
    model = AdvancedNote
    template_name = 'tools/notes/notes_detail.html'
    context_object_name = 'note'


class NotesCreateView(LoginRequiredMixin, CreateView):
    model = AdvancedNote
    template_name = 'tools/notes/notes_form.html'
    fields = ['title', 'content', 'tags', 'is_favorite', 'checklist']
    success_url = reverse_lazy('notes:notes_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = AdvancedNote
    template_name = 'tools/notes/notes_form.html'
    fields = ['title', 'content', 'tags', 'is_favorite', 'checklist']
    success_url = reverse_lazy('notes:notes_list')

    def get_queryset(self):
        return AdvancedNote.objects.filter(user=self.request.user)


class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = AdvancedNote
    template_name = 'tools/notes/notes_confirm_delete.html'
    success_url = reverse_lazy('notes:notes_list')
    context_object_name = 'note'

    def get_queryset(self):
        return AdvancedNote.objects.filter(user=self.request.user)


def note_share_view(request, note_id):
    note = get_object_or_404(AdvancedNote, pk=note_id)
    return render(request, 'tools/notes/notes_detail.html', {'note': note})


def quote_of_the_day(request):
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        data = response.json()
        daily_quote_text = data[0]['q']
        author_name = data[0]['a']
    except requests.exceptions.RequestException:
        daily_quote_text = "API se quote load nahi ho paya. Kripya baad mein prayas karein."
        author_name = "System"
    except (KeyError, IndexError):
        daily_quote_text = "API mein ek error hua."
        author_name = "System"
    
    submitted_quotes_list = Quote.objects.filter(is_approved=True)
    unapproved_quotes = []
    if request.user.is_authenticated:
        unapproved_quotes = Quote.objects.filter(created_by=request.user, is_approved=False)

    return render(request, 'tools/quotes/quotes_day.html', {
        'daily_quote': {'text': daily_quote_text, 'author': author_name},
        'submitted_quotes_list': submitted_quotes_list,
        'unapproved_quotes': unapproved_quotes,
    })

class QuoteCreateView(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'tools/quotes/quotes_form.html'
    fields = ['text', 'author']
    success_url = reverse_lazy('tools:quote_of_the_day')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.is_approved = False
        return super().form_valid(form)
    
class QuoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Quote
    template_name = 'tools/quotes/quotes_form.html'
    fields = ['text', 'author']
    success_url = reverse_lazy('tools:quote_of_the_day')

    def get_queryset(self):
        # Sirf quote ke owner ko hi update karne ki permission de
        return Quote.objects.filter(created_by=self.request.user)


class QuoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Quote
    template_name = 'tools/quotes/quotes_confirm_delete.html'
    success_url = reverse_lazy('tools:quote_of_the_day')
    context_object_name = 'quote'

    def get_queryset(self):
        # Sirf quote ke owner ko hi delete karne ki permission de
        return Quote.objects.filter(created_by=self.request.user)


@login_required
@csrf_exempt
def vote_quote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        vote_type = request.POST.get('vote_type')
        
        try:
            quote = Quote.objects.get(pk=quote_id)
            QuoteVote.objects.update_or_create(
                user=request.user,
                quote=quote,
                defaults={'vote_type': vote_type}
            )
            
            return JsonResponse({'status': 'success', 'message': 'Vote recorded.'})
        except Quote.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Quote not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})