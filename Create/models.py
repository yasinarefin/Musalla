from django.db import models
from Quiz.models import *
import uuid
# Create your models here.

def get_upload_path(self, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'quiz/{self.quiz.id}/{filename}'

class Image(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)

    
