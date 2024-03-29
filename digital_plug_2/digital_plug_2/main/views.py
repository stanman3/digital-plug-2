from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import CreateView

from digital_plug_2.main.decorators import unauthenticated_user, allowed_users, admin_only
from digital_plug_2.main.forms import ProjectForm, CreateUserForm, CreatorForm
from digital_plug_2.main.models import Project, Creator
from django.contrib import messages
from django.contrib.auth import authenticate, login as log, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


def get_creator():
    profiles = Creator.objects.all()
    if profiles:
        return profiles[0]
    return None


@login_required(login_url='login')
@admin_only
def dashboard(request):
    creators = Creator.objects.all()
    projects = Project.objects.all()
    creator_count = len(creators)
    project_count = len(projects)
    context = {
        'creators': creators,
        'projects': projects,
        'creator_count': creator_count,
        'project_count': project_count,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'creator'])
def show_home(request):
    if request.user.is_superuser:
        return redirect('dashboard')
    creator = get_creator()
    if creator:
        projects = request.user.creator.project_set.all()[::-1]
        project_1 = ''
        project_2 = ''
        if projects:
            if len(projects) >= 2:
                project_1 = projects[0]
                project_2 = projects[1]

            else:
                project_1 = projects[0]
        context = {
            'creator': creator,
            'projects': projects,
            'project_1': project_1,
            'project_2': project_2,
        }
        return render(request, 'home.html', context)
    else:
        return redirect('show index')


class ShowIndex(views.TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(ShowIndex, self).dispatch(request, *args, **kwargs)


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            log(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username/Password is incorrect')

    context = {

    }
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='creator')
            user.groups.add(group)
            Creator.objects.create(
                user=user,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def creator_details(request, pk):
    if not request.user.is_superuser and not request.user.is_anonymous:
        return redirect('profile details')
    creator = Creator.objects.get(pk=pk)
    projects = creator.project_set.all()[::-1]
    even_pr = []
    odd_pr = []
    for i in range(len(projects)):
        if i % 2 == 0:
            even_pr.append(projects[i])
        else:
            odd_pr.append(projects[i])

    context = {
        'creator': creator,
        'projects': projects,
        'even_pr': even_pr,
        'odd_pr': odd_pr,
    }
    return render(request, 'creator-details.html', context)


def explore(request):
    projects = Project.objects.all()[::-1]
    even_pr = []
    odd_pr = []
    for i in range(len(projects)):
        if i % 2 == 0:
            even_pr.append(projects[i])
        else:
            odd_pr.append(projects[i])

    context = {
        'projects': projects,
        'even_pr': even_pr,
        'odd_pr': odd_pr,
    }
    return render(request, 'explore.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['creator'])
def profile_details(request):
    creator = request.user.creator
    projects = request.user.creator.project_set.all()[::-1]
    even_pr = []
    odd_pr = []
    for i in range(len(projects)):
        if i % 2 == 0:
            even_pr.append(projects[i])
        else:
            odd_pr.append(projects[i])

    context = {
        'creator': creator,
        'projects': projects,
        'even_pr': even_pr,
        'odd_pr': odd_pr,
    }
    return render(request, 'profile-creator.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['creator'])
def profile_edit(request):
    creator = request.user.creator
    form = CreatorForm(instance=creator)

    if request.method == 'POST':
        form = CreatorForm(request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            return redirect('profile details')

    context = {
        'form': form,
    }
    return render(request, 'edit-profile-creator.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def creator_edit(request, pk):
    creator = Creator.objects.get(pk=pk)
    form = CreatorForm(instance=creator)
    if request.method == 'POST':
        form = CreatorForm(request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            return redirect('creator details', creator.pk)

    context = {
        'form': form,
        'creator': creator,
    }
    return render(request, 'edit-creator.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['creator'])
def profile_delete(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')

    context = {
        'user': user,
    }
    return render(request, 'delete-profile-creator.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def creator_delete(request, pk):
    creator = Creator.objects.get(pk=pk)
    if request.method == 'POST':
        creator.user.delete()
        return redirect('dashboard')
    context = {
        'creator': creator,
    }
    return render(request, 'delete-creator.html', context)


class UploadView(CreateView):
    model = Project
    template_name = 'upload-project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class ProjectDetails(views.DetailView):
    model = Project
    template_name = 'single-post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object
        context['creator'] = self.object.creator
        return context


class EditProject(views.UpdateView):
    model = Project
    template_name = 'edit-project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('profile details')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class DeleteProject(views.DeleteView):
    model = Project
    template_name = 'delete-project.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


def about(request):
    return render(request, 'about.html')

