from django import template
from Quiz.models import *
from Participate.models import *
from django.db.models import Sum
register = template.Library()

# returns submitted answer and correct answer
@register.filter
def get_total_points(quiz_obj):
    return Question.objects.filter(quiz=quiz_obj).aggregate(Sum('points'))['points__sum']


register.filter('total_points', get_total_points)