from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile_list', ),
    path('create/', views.profile_create, name='profile_create', ),
    path('<int:profile_id>/show/', views.profile_show, name='profile_show', ),
    path('<int:profile_id>/edit/', views.profile_edit, name='profile_edit', ),
]