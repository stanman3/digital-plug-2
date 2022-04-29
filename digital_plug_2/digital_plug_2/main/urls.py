from django.urls import path

from digital_plug_2.main.views import show_index, show_home, login, register, profile_details, profile_edit, \
    profile_delete, upload_project, project_details, delete_project, about, logout_user, dashboard, \
    explore, creator_details, creator_edit, creator_delete, EditProject

urlpatterns = (
    path('', show_home, name='home'),
    path('home/', show_index, name='show index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('explore/', explore, name='explore'),

    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),

    path('creator/details/<int:pk>/', creator_details, name='creator details'),
    path('creator/edit/<int:pk>/', creator_edit, name='creator edit'),
    path('creator/delete/<int:pk>/', creator_delete, name='creator delete'),

    path('profile/details/', profile_details, name='profile details'),
    path('profile/edit/', profile_edit, name='profile edit'),
    path('profile/delete/', profile_delete, name='profile delete'),

    path('project/upload/<int:pk>/', upload_project, name='upload project'),
    path('project/details/<int:pk>/', project_details, name='project details'),
    path('project/edit/<int:pk>/', EditProject.as_view(), name='edit project'),
    path('project/delete/<int:pk>/', delete_project, name='delete project'),

    path('about/', about, name='about'),
)