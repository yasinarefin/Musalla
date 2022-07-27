
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from Quiz.models import *
from User.models import *
from Participate.models import *
from django.db.models import Count, Sum, Q
# Create your views here.


def leaderboard_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")

    user_obj = request.user 
    quiz_obj = Quiz.objects.get(id = quiz_id)
    leaderboard = Submission.objects.filter(
        quiz= quiz_obj
    ).values("user__username").annotate(score=Sum('points')).order_by("-score")

    opp = Question.objects.filter(quiz__id=1).values(
        "question_text").annotate(submitted=Count("submission__user"))

    for i in opp:
        print(i)
    return render(request, "leaderboard.html", {
        "quiz" : quiz_obj,
        "leaderboard" : leaderboard,
    })