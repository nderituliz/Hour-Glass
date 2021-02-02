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

@login_required(login_url='/accounts/login/')
def updateprofile(request):
    diary = Diary.objects.all()
    posts = Profile.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been successfully updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'user_form':user_form,
    'profile_form':profile_form,
    'posts':posts,
    'diary':diary,
    }

    return render(request, 'profile/update_profile.html', context)

@login_required(login_url='/accounts/login/')
def postsubject(request):
    current_user = request.user
    if request.method == 'POST':
        form = SubjectForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.author = current_user
            subject.save()
        return redirect('/')
    else:
        form = SubjectForm()
    context = {
        'form':form,
    }
    return render(request, 'PostSubject.html', context)

@login_required(login_url='/accounts/login/')
def get_diary(request, id):
    diary = Diary.objects.get(pk=id)
    return render(request, 'diary.html', {'diary':diary)

@login_required(login_url='/accounts/login/')
def search_diary(request):
    if 'diary' in request.GET and request.GET['diary']:
        search_term = request.GET["diary"]
        searched_diary = Diary.search_diary(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message, "diary": searched_diary})
    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html', {"message":message})
