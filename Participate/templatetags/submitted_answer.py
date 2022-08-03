from django import template
from Quiz.models import *
from Participate.models import *
register = template.Library()

# returns submitted answer and correct answer
@register.filter
def get_submitted_answer(user, question_id):
    question_obj = Question.objects.get(id=question_id)
    if question_obj.question_type == "single_choice":
        return Submission.objects.get(user=user, question=question_obj).answer
    elif question_obj.question_type == "multiple_choice":
        return Submission.objects.get(user=user, question=question_obj).answer
    elif question_obj.question_type == "value_input":
        pass


register.filter('submitted_answer', get_submitted_answer)