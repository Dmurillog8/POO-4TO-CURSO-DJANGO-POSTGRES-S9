from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegisterForm

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")