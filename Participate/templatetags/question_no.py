from django import template
from Quiz.models import *
from Participate.models import *
from Participate.helper import *
register = template.Library()

@register.filter
def question_no(question_id):
    return get_question_no(question_id)
    

register.filter('question_no', question_no)