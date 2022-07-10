from django.contrib import admin
from django.urls import path, include
from Create.views import createnew_view, add_question_view, questions_view, delete_question_view
urlpatterns = [
    path('new/', createnew_view, name ="createnew"),
    path('<int:quiz_id>/questions/', questions_view, name="questions"),
    path('<int:quiz_id>/add-question/', add_question_view, name="add-question"),
    path('<int:quiz_id>/delete-question/', delete_question_view, name="delete-question"),
]
