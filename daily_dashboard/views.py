from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

def daily_dashboard_index(request):
    return render(request, 'daily_dashboard/index.html')

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


def permission_denied(request):
    return render(request, 'permission_denied.html')