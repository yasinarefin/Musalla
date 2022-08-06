
from django.urls import path, include
from Stats.views import *

app_name = "Stats"
urlpatterns = [
    path('leaderboard/<int:quiz_id>/', leaderboard_view, name="leaderboard"),
    path('statistics/<int:quiz_id>/', statistics_view, name="statistics"),
]
