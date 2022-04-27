from django.contrib import admin
from digital_plug_2.main.models import Project, Creator, Category

# Register your models here.
admin.site.register(Project)

admin.site.register(Creator)

admin.site.register(Category)