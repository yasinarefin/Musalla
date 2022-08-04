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


class Clarification(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    asked_by = models.ForeignKey(MusallaUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    is_answered = models.BooleanField(default=False)
    answer = models.CharField(max_length=500)
    

    class Meta:
        indexes = [
            models.Index(fields=['quiz', 'question']),
        ]


    
