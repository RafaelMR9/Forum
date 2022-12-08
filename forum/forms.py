from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Topic

class TopicModel2Form(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'tags']

class UserModel2Form(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']