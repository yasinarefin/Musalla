
from django.urls import path, include
from Quiz.views import *

app_name = "Quiz"
urlpatterns = [
    path('category/<int:id>/', category_view, name="category-page"),
    path('search/', search_view, name="search-quiz"),
   # path('list/', quiz_list_view, name="quiz-list"),
]
