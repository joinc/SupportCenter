from django.urls import path
from . import profile

urlpatterns = [
    path('list/', profile.profile_list, name='profile_list', ),
    path('<int:profile_id>/show/', profile.profile_show, name='profile_show', ),
    path('<int:profile_id>/edit/', profile.profile_edit, name='profile_edit', ),
]