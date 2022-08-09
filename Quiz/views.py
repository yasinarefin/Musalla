
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from Quiz.models import *
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
# Create your views here.


def home_view(request):
    return render(request, "index.html", {
        "categories":Category.objects.all()
    })

def category_view(request, id):
    page_no = request.GET.get("page", 1)
    paginator = None
    if id > 0: # specific category
        paginator = Paginator(Quiz.objects.filter(category=id).order_by("id"), 4)    
    else:
        paginator = Paginator(Quiz.objects.all().order_by("id"), 4)    

    return render(request, "category.html", {
        "quiz_page": paginator.get_page(page_no),
        "categories":Category.objects.all(),
        "category_name" : "All" if id == 0 else Category.objects.filter(id=id).first().name
    })

def search_view(request):
    query = request.GET.get("search", "")

    page_no = request.GET.get("page", 1)
    paginator = None

    if query.isdigit(): 
        paginator = Paginator(Quiz.objects.filter(id=int(query)).order_by("id"), 4)
    else:
        paginator = Paginator(Quiz.objects.filter(name__icontains=query).order_by("id"), 4)

    return render(request, "quiz_list.html", {
        "quiz_page": paginator.get_page(page_no),
        "categories":Category.objects.all(),
        "title" : query + " -search"
    })
