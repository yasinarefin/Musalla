from django.contrib import admin
from django.urls import path, include
from .views import login_view, signup_view, logout_view

app_name = "User"
urlpatterns = [
    path('login/',  login_view, name="login"),
    path('signup/',  signup_view, name="signup"),
    path('logout/',  logout_view, name="logout"),
]