from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from .forms import LoginForm, SignupForm

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return HttpResponse("Fuck")
            else:
                return HttpResponse("Fuck me")
    context = {"login_form": form}
    return render(request, "login.html", context)


def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponse("Fuck")
        else:
            return HttpResponse("Fuck me")
    context = {"signup_form": form}
    return render(request, "signup.html", context)
