from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from Quiz.models import *
from .forms import LoginForm, SignupForm
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse

def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect(request.GET.get('next',"/"))
            else:
                return render(request, "login.html", {"login_form":form})
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
            return render(request, "signup.html", {"signup_form":form})
    context = {"signup_form": form}
    return render(request, "signup.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def dashboard_view(request):
    pass

def dashboard_creation_view(request):
    if request.user.is_authenticated == False:
        return redirect("User:login")


    context ={
        "created_quizzes" : Quiz.objects.filter(creator=request.user),
        "categories":Category.objects.all()
    }

    return render(request, "dashboard_creation.html", context)

    