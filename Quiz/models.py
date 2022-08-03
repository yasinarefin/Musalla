from django.db import models
from User.models import MusallaUser
from django.utils import timezone
from tinymce import models as tinymce_models
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

    PUBLIC = 'public'
    PRIVATE = 'private'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
    ]
    visibility = models.CharField(
        max_length=7,
        choices=VISIBILITY_CHOICES,
        default=PUBLIC
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_status(self):
        if self.start_time > timezone.now():
            return 'upcoming'
        elif self.end_time < timezone.now():
            return 'ended'
        else:
            return 'running'

    def __str__(self):
        return self.name



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    question_type = models.CharField(max_length=20) # single choice, multiple choice or value
    question_text = tinymce_models.HTMLField()
    points = models.PositiveIntegerField()
    options = models.JSONField()
    answer = models.JSONField()

    def __str__(self):
        return str(self.id)


class AllowedUser(models.Model):
    quiz = models.ForeignKey(Quiz,  models.CASCADE)
    user = models.ForeignKey(MusallaUser, models.CASCADE)


