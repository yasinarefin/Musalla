from django import template
from Quiz.models import *
from Participate.models import *
register = template.Library()

# returns submitted answer and correct answer
@register.filter
def get_correct_answer(question_id):
    return Question.objects.get(id=question_id).answer


register.filter('correct_answer', get_correct_answer)