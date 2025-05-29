from django.shortcuts import render
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'original_name/login.html'

class RegisterView(TemplateView):
    template_name = 'original_name/register.html' 