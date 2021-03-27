from django.urls import path
# from .views import homePageView
from . import views
from .views import TaskListView
from .models import Task 

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('sent', views.sentView, name='sent'),
    path('simpleForm', views.simpleForm, name='simpleForm'),
    path('taskList', TaskListView.as_view(), name='taskList') # ,
    # path('task/<int:pk>', TaskDetailView.as_view(), name='taskNumber')
]
