from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grade']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grade']
