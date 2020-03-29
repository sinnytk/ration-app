from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from .forms import CustomUserCreationForm
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('signup-successful')
    template_name = 'users/register.html'

def sign_up_successful(request):
    return HttpResponse('Your account has been successfully registered, ask admin to approve your registration before logging in')