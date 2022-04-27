from django.shortcuts import render, redirect
from digital_plug_2.main.forms import ProjectForm
from digital_plug_2.main.models import Project, Creator
from django.contrib.auth.forms import UserCreationForm


def get_creator():
    profiles = Creator.objects.all()
    if profiles:
        return profiles[0]
    return None


def show_home(request):
    creator = get_creator()
    if creator:
        projects = creator.project_set.all()
        context = {
            'creator': creator,
            'projects': projects,
        }
        return render(request, 'home.html', context)
    else:
        return redirect('show index')


def show_index(request):
    creator = get_creator()
    if creator:
        return redirect('home')
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    form = UserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def profile_details(request):
    return render(request, 'profile-creator.html')


def profile_edit(request):
    return render(request, 'edit-profile-creator.html')


def profile_delete(request):
    return render(request, 'delete-profile-creator.html')


def upload_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm()
    context = {
        'form': form,
    }
    return render(request, 'upload-project.html', context)


def project_details(request, pk):
    project = Project.objects.get(pk=pk)
    context = {
        'project': project,
    }
    return render(request, 'single-post.html', context)


def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'edit-project.html', context)


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')

    context = {
        'project': project,
    }
    return render(request, 'delete-project.html', context)


def about(request):
    return render(request, 'about.html')

