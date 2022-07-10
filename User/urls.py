from django.contrib import admin
from django.urls import path, include
from .views import login_view, signup_view, logout_view, dashboard_view, dashboard_creation_view

app_name = "User"
urlpatterns = [
    path('login/',  login_view, name="login"),
    path('signup/',  signup_view, name="signup"),
    path('logout/',  logout_view, name="logout"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('dashboard/creation/', dashboard_creation_view, name="dashboard-creation"),

]