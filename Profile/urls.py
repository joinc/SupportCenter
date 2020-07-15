from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile_list', ),
    path('<int:profile_id>/show/', views.profile_show, name='profile_show', ),
    path('<int:profile_id>/edit/', views.profile_edit, name='profile_edit', ),
]