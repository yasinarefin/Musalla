from django.contrib import admin
from User.models import MusallaUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(MusallaUser, UserAdmin)