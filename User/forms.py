from django import forms
from django.core.validators import RegexValidator
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from User.models import MusallaUser


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=50,
        widget = forms.TextInput(
            attrs={
                "type":"text", "class":"form-control",  "id":"username", "placeholder":"Enter username"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "type" : "password", "class" : "form-control" , "id" :"password",  "placeholder" :"Password"
            }
        )
    )

    @transaction.atomic
    def save(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            return user
        else:
            return False


class SignupForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"text", "class":"form-control",  "id":"username", "placeholder":"Enter username"
            }
        ),
    )

    password1 = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "type" : "password", "class" : "form-control" , "id" :"password",  "placeholder" :"Password"
            }
        ),
    )
    password2 = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "type" : "password", "class" : "form-control" , "id" :"password2",  "placeholder" :"Confirm password"
            }
        ),
    ),

    first_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"text", "class":"form-control",  "id":"f-name", "placeholder":"First name"
            }
        ),
    )
    last_name = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"text", "class":"form-control",  "id":"l-name", "placeholder":"Last name"
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "type":"text", "class":"form-control",  "id":"email", "placeholder":"Email"
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = MusallaUser
        fields = [
            "password1",
            "password2",
            "username",
            "first_name",
            "last_name",
            "email"
        ]

    @transaction.atomic
    def save(self):
        # print(self.cleaned_data)
        user = super().save(commit=False)
        user.save()
        return True