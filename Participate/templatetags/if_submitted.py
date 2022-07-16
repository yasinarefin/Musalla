from django import template
from Quiz.models import *
from Participate.models import *
register = template.Library()

@register.filter
def check_if_submitted(user, question_id):
    if Submission.objects.filter(user=user, question=Question.objects.get(id=question_id)).exists():
        return True
    return False

register.filter('if_submitted', check_if_submitted)