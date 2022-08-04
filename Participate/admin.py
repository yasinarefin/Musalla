from django.contrib import admin
from .models import *
# Register your models here.

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'points')
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Clarification)