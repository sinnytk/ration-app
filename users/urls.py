from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('signup/sucessful',views.sign_up_successful,name='signup-successful'),
    path('signup/',views.SignUp.as_view(), name='signup')
]
