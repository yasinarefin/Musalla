from django.db import models
from User.models import MusallaUser
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    creator = models.ForeignKey(MusallaUser, models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.ForeignKey(Category, models.CASCADE)
    visibility = models.CharField(max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    question_type = models.CharField(max_length=20) # single choice, multiple choice or value
    question_text = models.TextField()
    points = models.PositiveIntegerField()
    options = models.JSONField()
    answer = models.JSONField()


class AllowedUser(models.Model):
    quiz = models.ForeignKey(Quiz,  models.CASCADE)
    user = models.ForeignKey(MusallaUser, models.CASCADE)


