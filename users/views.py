from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .forms import CustomUserLoginForm

from .forms import CustomUserCreationForm
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('signup-successful')
    template_name = 'users/register.html'
class CustomUserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form=CustomUserLoginForm

def sign_up_successful(request):
    return HttpResponse('Your account has been successfully registered, ask admin to approve your registration before logging in')