from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Quiz)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_type', 'points')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
admin.site.register(AllowedUser)