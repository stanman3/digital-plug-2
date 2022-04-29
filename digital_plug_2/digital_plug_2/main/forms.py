from django.forms import ModelForm
from digital_plug_2.main.models import Project, Creator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreatorForm(ModelForm):
    class Meta:
        model = Creator
        fields = ('first_name', 'last_name', 'age', 'country', 'image')


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'category', 'description', 'image', 'creator')
        widgets = {
            'category': forms.CheckboxSelectMultiple,
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')