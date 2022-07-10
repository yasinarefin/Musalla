
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from Quiz.models import *
from django.utils.dateparse import parse_datetime
# Create your views here.


def home_view(request):
    return render(request, "index.html")