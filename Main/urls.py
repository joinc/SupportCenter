from django.urls import path
from Main import views, configure

urlpatterns = [
    path('', views.index, name='index', ),
    path('login/', views.login, name='login', ),
    path('logout/', views.logout, name='logout', ),
    path('configure/list/', configure.configure_list, name='configure_list', ),
    path('configure/preset/create/', configure.preset_create, name='preset_create', ),
    path('configure/preset/list/', configure.preset_list, name='preset_list', ),
    path('configure/preset/<int:preset_id>/edit/', configure.preset_edit, name='preset_edit', ),
    path('configure/preset/<int:preset_id>/delete/', configure.preset_delete, name='preset_delete', ),
]
