from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from Quiz.models import *
from Participate.models import *
import json
from django.utils.dateparse import parse_datetime
from django.urls import reverse
import datetime as dt
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

# Create your views here.


def questions_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")
    quiz_obj = Quiz.objects.get(id=quiz_id)

    if quiz_obj.visibility == 'private':
        try:
            AllowedUser.objects.get(
                quiz=quiz_obj,
                user=request.user
            )
        except:
            return HttpResponse(
                "Not authorized for this quiz",
                status=401
            )

    # first_time = dt.datetime().now()
    # later_time = dt.datetime(quiz_obj.end_time)
    # difference = later_time - first_time


    #print(max((quiz_obj.end_time - timezone.now()).total_seconds(),0))

    if quiz_obj.get_status == "upcoming":
        return render(request, "upcoming_quiz.html", {
            "quiz":quiz_obj,
            "time_remaining":max((quiz_obj.start_time - timezone.now()).total_seconds(),0)
        })

    return render(request, "view_questions.html", {
        "questions": Question.objects.filter(quiz=quiz_id),
        "submitted_answers": Submission.objects.filter(quiz=quiz_obj, user=request.user),
        "quiz": quiz_obj,
        "points": Submission.objects.filter(quiz=quiz_obj, user=request.user).aggregate(Sum("points"))["points__sum"],
        "time_remaining": max((quiz_obj.end_time - timezone.now()).total_seconds(),0)
    })

# rest endpoint

def submit_view(request, question_id):
    if request.user.is_authenticated == False:
        return HttpResponse(
            json.dumps({"msg": "Not authorized"}),
            content_type="application/json",
            status=401
        )

    question_obj = Question.objects.get(id=question_id)
    quiz_obj = Quiz.objects.get(id=question_obj.quiz.id)

    if quiz_obj.visibility == "private":
        if AllowedUser.objects.filter(quiz=quiz_obj, user=request.user).exists() == False:
            return HttpResponse(
                json.dumps({"msg": "Not authenticated for this quiz"}),
                content_type="application/json",
                status=403
            )

    if quiz_obj.get_status in ['upcoming', 'ended']:
        return HttpResponse(
            json.dumps({"msg": "Quiz is not running"}),
            content_type="application/json",
            status=403
        )

    if Submission.objects.filter(user=request.user, question=question_obj).exists():
        return HttpResponse(
            json.dumps({"msg": "Already submitted"}),
            content_type="application/json",
            status=208
        )

    if request.method == "POST":
        answer = json.loads(request.POST.get("answer"))

        validator = ValidateAnswer(answer, question_obj)

        if validator.isValid:
            Submission.objects.create(
                user=request.user,
                quiz=quiz_obj,
                question=question_obj,
                answer=answer,
                points=validator.points
            )
        else:
            return HttpResponse(
                json.dumps({"msg": "Invalid submission"}),
                content_type="application/json",
                status=406
            )

        return HttpResponse(
            json.dumps({"msg": "Submitted"}),
            content_type="application/json",
            status=200
        )


class ValidateAnswer():
    def __init__(self, answer, question_obj):
        self.answer = answer
        self.question_obj = question_obj
        self.isValid = False
        self.points = 0

        if question_obj.question_type == "single_choice":
            if self.validate_single_choice():
                self.isValid = True
        elif question_obj.question_type == "multiple_choice":
            if self.validate_multiple_choice():
                self.isValid = True

    def validate_single_choice(self):
        if len(self.answer) == 1 and self.answer[0] < len(self.question_obj.options):
            if self.answer[0] == self.question_obj.answer[0]:
                self.points = self.question_obj.points
            return True
        return False

    def validate_multiple_choice(self):
        if len(self.answer) > 0 and max(self.answer) < len(self.question_obj.options):
            if len(self.answer) == len(self.question_obj.answer) and all(i in self.question_obj.answer for i in self.answer): # evaluation
                self.points = self.question_obj.points
            return True
        return False