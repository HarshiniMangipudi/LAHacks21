from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView



from django.conf import settings


# from .forms import MessageForm
from .forms import ProfileUpdateForm
from .utils import send_msg

from django.views.generic import ListView, DetailView
from django.db import models
from .models import Task 

def homePageView(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'home.html')

    # return HttpResponse('Hello, World!')

# def sentView(request):
#     return HttpResponse('Sent!')

# def simpleForm(request):
#     # return HttpResponse('Hello, World!')
#     return render(request, 'pages/simpleForm.html')

# def simpleForm(request):
#     # return HttpResponse('Hello, World!')
#     # return render(request, 'pages/simpleForm.html')
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = MessageForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             msg = form.cleaned_data['your_msg']
#             send_msg(msg)
#             print(f"success! sent: {msg}")

#             return HttpResponseRedirect('/sent')
#         print("invalid form!")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = MessageForm()

#     return render(request, 'simpleForm.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class UserLogin(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    next = '/'

def logout_view(request):
    logout(request)
    return redirect('login')

def profileUpdateView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            form.save()
            return redirect('profileUpdate')
        print("invalid form!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profileUpdateForm.html', {'form': form})

def taskListViews(request):
    context = {
        'tasks' : Task.objects.all()
    }
    return render(request, 'taskList.html', context)

class TaskListView(ListView):
    model = Task; 
    template_name = 'taskList.html'
    context_object_name = 'tasks'

def task_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# def 