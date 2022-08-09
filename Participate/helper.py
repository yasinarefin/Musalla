from Quiz.models import *
from Participate.models import *
from django.db.models import Sum
def get_question_no(ques_obj):
    quiz_obj = ques_obj.quiz

    questions_obj = Question.objects.filter(quiz= quiz_obj)

    for idx, question in enumerate(questions_obj, start=1):
        if question.id == ques_obj.id:
            return idx


def get_user_points(quiz_obj, user_obj):
    return Submission.objects.filter(quiz=quiz_obj, user=user_obj).aggregate(Sum("points"))["points__sum"]
