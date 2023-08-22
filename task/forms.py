from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from task.models import UserProfile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1',"password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'