from django.db import models
from Quiz.models import *
from User.models import MusallaUser
# Create your models here.


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(MusallaUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    answer = models.JSONField()
    points = models.IntegerField()


    
