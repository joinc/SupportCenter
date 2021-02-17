from django.urls import path
from Main import views, configure

urlpatterns = [
    path('', views.index, name='index', ),
    path('login/', views.login, name='login', ),
    path('logout/', views.logout, name='logout', ),
    path('configure/list/', configure.configure_list, name='configure_list', ),
    path('configure/preset/list/', configure.preset_list, name='preset_list', ),
]
