
from django.urls import path, include
from Quiz.views import *

app_name = "Quiz"
urlpatterns = [
    path('', home_view, name="home-page"),
]
