from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse


def log_in(request: HttpRequest):
    if request.method == "GET":
        return render(request, "original_name/login.html")
    # This view only support GET and POST
    if request.method != "POST":
        return HttpResponseForbidden()

    email = request.POST["email"]
    password = request.POST["password"]

    user: User | None = authenticate(
        request, email=email, username=email, password=password
    )
    if not user:
        return HttpResponseForbidden()

    login(request, user)
    return redirect(reverse("pages:home"), permanent=True, preserve_request=True)


def register(request: HttpRequest):
    if request.method == "GET":
        return render(request, "original_name/register.html")
    if request.method != "POST":
        return HttpResponseForbidden()

    email = request.POST["email"]
    password = request.POST["password"]

    user = User.objects.create_user(username=email, email=email, password=password)
    user.save()
    login(request, user)
    return redirect(reverse("pages:home"), permanent=True, preserver_request=True)
