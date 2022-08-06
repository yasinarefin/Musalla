from django.contrib import admin
from django.urls import path, include
from Create.views import createnew_view, add_question_view, edit_questions_view, delete_question_view, upload_view

app_name = "Create"

urlpatterns = [
    path('new/', createnew_view, name ="create-new"),
    path('<int:quiz_id>/edit-questions/', edit_questions_view, name="edit-questions"),
    path('<int:quiz_id>/add-question/', add_question_view, name="add-question"),
    path('<int:quiz_id>/delete-question/', delete_question_view, name="delete-question"),
    path('<int:quiz_id>/upload/', upload_view, name="upload"),
]
