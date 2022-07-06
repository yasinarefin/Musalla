from django.contrib import admin
from django.urls import path, include
from .views import login_view, signup_view
urlpatterns = [
    path('login/',  login_view, name="login"),
    path('signup/',  signup_view, name="signup"),
]