
from django.urls import path, include
from Participate.views import *

app_name = "Participate"
urlpatterns = [
    path('questions/<int:quiz_id>/', questions_view, name="view-questions"),
    path('submit/<int:question_id>/', submit_view, name="submit-view"),
    path('clarification/<int:quiz_id>/', clarification_view, name="clarification"),
    path('clarification/answer/<int:clarification_id>/', answer_clarification_view, name="answer-clarification"),
    
]
