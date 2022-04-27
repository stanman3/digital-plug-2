from django.forms import ModelForm
from digital_plug_2.main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'category', 'description', 'image', 'creator')
