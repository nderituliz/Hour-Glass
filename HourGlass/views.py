from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView,DetailView,UpdateView,DeleteView

# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    diary = Diary.objects.all()
    context = {
    "diary":diary,
    }
    return render(request, 'index.html', locals())

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'registration/register.html', context)


