
from django.urls import path, include
from Participate.views import *

app_name = "Participate"
urlpatterns = [
    path('questions/<int:quiz_id>/', questions_view, name="view-questions"),
    path('submit/<int:question_id>/', submit_view, name="submit-view"),
]
