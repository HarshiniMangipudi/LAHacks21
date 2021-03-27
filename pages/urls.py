from django.urls import path
from django.conf.urls import url
# from .views import homePageView
from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    # path('sent', views.sentView, name='sent'),
    # path('simpleForm', views.simpleForm, name='simpleForm'),
    # actual paths below

    # path('signup', views.signup_view, name='signup'),
    url(r'^signup/$', views.signup_view, name='signup'),

    # path("login", views.login_view, name="login"),
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
    # path("logout", views.logout_view, name="logout"),
    url(r'^logout/$', views.logout_view, name='logout'),

    url(r'^profileUpdate/$', views.profileUpdateView, name='profileUpdate'),
]
