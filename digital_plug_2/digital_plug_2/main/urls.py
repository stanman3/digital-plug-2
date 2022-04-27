from django.urls import path

from digital_plug_2.main.views import show_index, show_home, login, register, profile_details, profile_edit, \
    profile_delete, upload_project, project_details, edit_project, delete_project, about

urlpatterns = (
    path('', show_home, name='home'),
    path('home/', show_index, name='show index'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/details/', profile_details, name='profile details'),
    path('profile/edit/', profile_edit, name='profile edit'),
    path('profile/delete/', profile_delete, name='profile delete'),

    path('project/upload/', upload_project, name='upload project'),
    path('project/details/<int:pk>/', project_details, name='project details'),
    path('project/edit/<int:pk>/', edit_project, name='edit project'),
    path('project/delete/<int:pk>/', delete_project, name='delete project'),

    path('about/', about, name='about'),
)