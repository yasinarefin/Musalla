from django import template
from Quiz.models import *
from Participate.models import *
from Participate.helper import *
from django.db.models import Sum
register = template.Library()

# returns score for a particular quiz of a user
@register.filter
def calculate_user_points(quiz_obj, user_obj):
    return get_user_points(quiz_obj, user_obj)

register.filter('user_points', calculate_user_points)