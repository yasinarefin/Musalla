from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from User.models import MusallaUser
from Quiz.models import *
from .forms import *
import json
from django.utils.dateparse import parse_datetime
from django.urls import reverse

# Create your views here.


def quiz_form_validator(field_values):
    errors = []
    start_date = parse_datetime(field_values["start_time"])
    end_date = parse_datetime(field_values["end_time"])

    if len(field_values["name"].strip()) < 5:
        errors.append("Name should be at least 5 characters")

    if start_date > end_date:
        errors.append("Start date cannot be greater than end date")

    try:
        Category.objects.get(name=field_values["category"])
    except:
        errors.append("Select category")

    if field_values["visibility"] in ["public", "private"]:
        pass
    else:
        errors.append("Select visibility")

    return errors


def createnew_view(request):

    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")

    field_values = {}
    fields = ["name", "start_time", "end_time", "category", "visibility"]
    errors = []

    for i in fields:
        field_values[i] = ""

    if request.method == "POST":
        for i in fields:
            field_values[i] = request.POST.get(i)
        errors = quiz_form_validator(field_values)

        if len(errors) == 0:
            obj = Quiz.objects.create(
                name=field_values["name"],
                start_time=field_values["start_time"],
                end_time=field_values["end_time"],
                visibility=field_values["visibility"],
                creator=request.user,
                category=Category.objects.get(name=field_values["category"])
            )
    context = {
        "categories": [category.name for category in Category.objects.all()],
        "quiz_create_form": field_values,
        "errors": errors,
    }
    return render(request, "create_new.html", context)


def edit_questions_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return redirect(f"{reverse('User:login')}?next={request.path}")
    quiz_obj = Quiz.objects.get(id=quiz_id)

    if quiz_obj.creator != request.user:
        return HttpResponse("You are not authorized to edit the quiz")

    if request.method == "POST":
        questions_arr = json.loads(request.POST.get("questions"))

        for question in questions_arr:
            if Question.objects.get(id=question["id"]).quiz != quiz_obj:
                break
            Question.objects.filter(id=question["id"]).update(**question)
            
        return HttpResponse(
            json.dumps({"msg": "ok"}),
            content_type="application/json",
            status=200
        )

    return render(
        request,
        "edit_questions.html",
        {
            "quiz_id": quiz_id,
            "quiz_name": quiz_obj.name,
            "questions": Question.objects.filter(quiz=quiz_obj)
        }
    )


# rest api endpoint to add question
def add_question_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return HttpResponse(
            "Not authenticated",
            status=401
        )

    quiz_obj = Quiz.objects.get(id=quiz_id)

    if quiz_obj.creator != request.user:
        return HttpResponse("You are not authorized to edit the quiz")

    if request.method == "POST":
        question_type = request.POST.get("question_type")
        print(question_type)

        if question_type in ["single_choice", "multiple_choice"] == False:
            return HttpResponse(
                "Invalid",
                status=401
            )

        try:
            question_obj = Question.objects.create(
                quiz=quiz_obj,
                question_text="",
                question_type=question_type,
                points=1,
                options=[],
                answer=[]
            )
            return HttpResponse(
                json.dumps({"id": str(question_obj.id)}),
                content_type="application/json",
                status=200
            )
        except:
            return HttpResponse(
                json.dumps({"msg": "Not Created"}),
                content_type="application/json",
                status=204
            )


def delete_question_view(request, quiz_id):
    if request.user.is_authenticated == False:
        return HttpResponse(
            "Not authenticated",
            status=401
        )

    quiz_obj = Quiz.objects.get(id=quiz_id)

    if quiz_obj.creator != request.user:
        return HttpResponse(
            json.dumps({"msg": "You are not authorized to edit the quiz"}),
            content_type="application/json",
            status=403
        )

    if request.method == "POST":
        question_id = request.POST.get("id")
        print("id", question_id)
        Question.objects.filter(id=question_id).delete()

        return HttpResponse(
            json.dumps({"msg": "deleted"}),
            content_type="application/json",
            status=204
        )