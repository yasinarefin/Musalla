
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from Quiz.models import *
from User.models import *
from Participate.models import *
from django.db.models import Count, Sum, Q, Max, Avg
# Create your views here.


def leaderboard_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")

    user_obj = request.user 
    quiz_obj = Quiz.objects.get(id = quiz_id)
    leaderboard = Submission.objects.filter(
        quiz= quiz_obj
    ).values("user__username").annotate(score=Sum('points')).order_by("-score")

    return render(request, "leaderboard.html", {
        "quiz" : quiz_obj,
        "leaderboard" : leaderboard,
        "points": Submission.objects.filter(quiz=quiz_obj, user=request.user).aggregate(Sum("points"))["points__sum"],
    })

def statistics_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")

    

    quiz_obj = Quiz.objects.get(id = quiz_id)
    max_points = Submission.objects.filter(quiz=quiz_obj).values("user").annotate(Sum("points")).aggregate(Max("points__sum")) 
    sum_points = Submission.objects.filter(quiz=quiz_obj).aggregate(Sum("points"))['points__sum']
    participants_count = Submission.objects.filter(quiz=quiz_obj).aggregate(Count('user',distinct=True), )['user__count']
    avg_points = sum_points / participants_count
    
    return render(request, "statistics.html", {
        "quiz" : quiz_obj,
        "points": Submission.objects.filter(quiz=quiz_obj, user=request.user).aggregate(Sum("points"))["points__sum"],
        "total_participants": Submission.objects.filter(quiz=quiz_obj).values("user__username").distinct().count(),
        "max_points":max_points["points__sum__max"]    ,
        "avg_points" : avg_points
        }
    )