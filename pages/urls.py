from django.urls import path
# from .views import homePageView
from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('sent', views.sentView, name='sent'),
    path('simpleForm', views.simpleForm, name='simpleForm'),
]
