"""Musalla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Quiz.views import home_view

app_name = "Musalla"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("User.urls") ),
    path('create/', include("Create.urls")),
    path('quiz/', include("Quiz.urls")),
    path('participate/', include("Participate.urls")),
    path('stats/', include("Stats.urls")),
    path('', home_view, name="home-page"),
    
]
