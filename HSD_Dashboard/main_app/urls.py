from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    #user accounts and profile
    path('accounts/signup/',views.signup, name='signup'),
    path('profile/',views.profile,name='profile')

]