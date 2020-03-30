from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/',views.CustomUserLoginView.as_view(),name='login'),
    path('signup/',views.SignUp.as_view(), name='signup'),
    path('signup/sucessful',views.sign_up_successful,name='signup-successful'),
    path('logout/',LogoutView.as_view(),name="logout")
]
