from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from django.conf import settings


# from .forms import MessageForm
from .forms import ProfileUpdateForm, TaskCreateForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db import models
from .models import Task 
from .forms import TaskForm

@login_required
def homePageView(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'home.html')

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
    redirect_field_name = '/home'

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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

@login_required
def taskListViews(request):
    context = {
        'tasks' : Task.objects.filter(user = request.user)
    }
    return render(request, 'taskList.html', context)

class TaskListView(ListView):
    model = Task; 
    template_name = 'taskList.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task 
    template_name = 'taskDescription.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task 
    form_class = TaskForm
    template_name = 'taskCreate.html'
    # fields = [
    #     'task_name',
    #     'body',
    #     'date_added',
    #     'date_due',
    #     'Sunday',
    #     'Monday',
    #     'Tuesday',
    #     'Wednesday',
    #     'Thursday',
    #     'Friday',
    #     'Saturday',
    #     'time_of_day',
    #     'friend_fb_id'
    # ]
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res = res.copy()
        res['custom_handled_fields'] = TaskForm.CUSTOM_HANDLED_FIELDS
        return res


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = TaskForm
    model = Task
    template_name = 'taskCreate.html'
    # fields = [
    #     'task_name',
    #     'body',
    #     'date_added',
    #     'date_due',
    #     'Sunday',
    #     'Monday',
    #     'Tuesday',
    #     'Wednesday',
    #     'Thursday',
    #     'Friday',
    #     'Saturday',
    #     'time_of_day',
    #     'friend_fb_id'
    # ]
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
 
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res = res.copy()
        res['custom_handled_fields'] = TaskForm.CUSTOM_HANDLED_FIELDS
        return res

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'taskDelete.html'
    success_url = '/'
    def test_func(self):
        task = self.get_object()
        return self.request.user == task.user


# class TaskCreateView(CreateView):
#     model = Task 
#     #need to add "due date" in fields 
#     fields = ['task name', 'task description']



## other way 
# def createTaskForm(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = TaskCreateForm(request.POST )
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # redirect to a new URL:
#             form.save()
#             return redirect('taskCreation')
#         print("invalid form!")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = TaskCreateForm()
#     return render(request, 'taskForm.html', {'form': form})

# def updateTaskForm(request, pk):
#     t = Task.objects.get(pk=pk)
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = TaskCreateForm(request.POST,instance=t)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # redirect to a new URL:
#             form.save()
#             return redirect('taskCreation')
#         print("invalid form!")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = TaskCreateForm(instance=t)
#     return render(request, 'taskForm.html', {'form': form})



# def task_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})


# def 


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
