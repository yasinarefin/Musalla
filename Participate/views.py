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

from dateutil.relativedelta import relativedelta

# Create your views here.


def questions_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")
    quiz_obj = Quiz.objects.get(id=quiz_id)

    if quiz_obj.visibility == 'private':
        try:
            AllowedUser.objects.get(quiz=quiz_obj, user=request.user)
        except:
            return HttpResponse("Not authorized for this quiz", status=401) 

    
    return render(request, "view_questions.html", {
        "questions": Question.objects.filter(quiz=quiz_id),
        "quiz": quiz_obj,
        "time_remaining": relativedelta(quiz_obj.end_time, quiz_obj.start_time)
    })

#rest endpoint
def submit_view(request, question_id):
    if request.user.is_authenticated == False:
        return HttpResponse(json.dumps({"msg":"Not authorized"}), content_type="application/json",status=401)
    
    question_obj = Question.objects.get(id=question_id)
    quiz_obj = Quiz.objects.get(id=question_obj.quiz.id)

    if quiz_obj.visibility == "private":
        if AllowedUser.objects.filter(quiz=quiz_obj, user=request.user).exists() == False:
            return HttpResponse(
                json.dumps({"msg":"Not authorized for this quiz"}),
                content_type="application/json",
                status=401
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
                json.dumps({"msg":"Invalid submission"}),
                content_type="application/json",
                status=200
            )

        return HttpResponse(
            json.dumps({"msg":"Submitted"}),
            content_type="application/json",
            status=200
        )


class ValidateAnswer():
    def __init__(self, answer, question_obj):
        self.answer = answer
        print(self.answer)
        self.question_obj = question_obj
        self.isValid = False

        if question_obj.question_type == "single_choice":
            if self.validate_single_choice():
                self.isValid = True

    def validate_single_choice(self):
        print("loko", len(self.answer))
        if len(self.answer) == 1 and self.answer[0] < len(self.question_obj.options):
            if self.answer[0] == self.question_obj.answer[0]:
                self.points = self.question_obj.points
            return True
        return False

    


    
