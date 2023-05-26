
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from Quiz.models import *
from User.models import *
from Participate.models import *
from django.db.models import Count, Sum, Q, Max, Avg
import json
import math
# Create your views here.


def leaderboard_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")
    quiz_obj = Quiz.objects.get(id = quiz_id)
    if quiz_obj.visibility == "private":
        if AllowedUser.objects.filter(quiz=quiz_id, user=request.user).exists() == False:
            return HttpResponse(
                json.dumps({"msg": "Not authenticated for this quiz"}),
                content_type="application/json",
                status=403
            )

    user_obj = request.user 
    
    leaderboard = Submission.objects.filter(
        quiz= quiz_id
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
    if quiz_obj.visibility == "private":
        if AllowedUser.objects.filter(quiz=quiz_id, user=request.user).exists() == False:
            return HttpResponse(
                json.dumps({"msg": "Not authenticated for this quiz"}),
                content_type="application/json",
                status=403
            )

    
    total_points = Question.objects.filter(quiz=quiz_obj).aggregate(Sum('points'))['points__sum']
    labels = []
    data = []

    for i in range(10):
        lab = total_points * ((i+1) * 10 / 100) 
        labels.append(str((i+1) * 10)+ "%")
        c = Submission.objects.filter(quiz=quiz_obj).values("user").annotate(Sum("points")).filter(points__sum__gte = math.ceil(lab)).count()
        
        data.append(c)
    
    max_points = Submission.objects.filter(quiz=quiz_obj).values("user").annotate(Sum("points")).aggregate(Max("points__sum")) 
    sum_points = Submission.objects.filter(quiz=quiz_obj).aggregate(Sum("points"))['points__sum']
    participants_count = Submission.objects.filter(quiz=quiz_obj).aggregate(Count('user',distinct=True), )['user__count']
    avg_points = 0 
    try:
        avg_points = sum_points / participants_count
    except:
        pass

    return render(request, "statistics.html", {
            "quiz" : quiz_obj,
            "points": Submission.objects.filter(quiz=quiz_id, user=request.user).aggregate(Sum("points"))["points__sum"],
            "total_participants": Submission.objects.filter(quiz=quiz_id).values("user__username").distinct().count(),
            "max_points":max_points["points__sum__max"]    ,
            "avg_points" : avg_points,
            "total_points" : total_points,
            "chart_data": json.dumps({
                "labels": labels,
                "data" : data,
                "step_size" : math.ceil(participants_count / 25) 
            }),
        
        }
    )