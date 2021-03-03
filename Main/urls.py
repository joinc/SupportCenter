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
    path('configure/address/create/', configure.address_create, name='address_create', ),
    path('configure/address/list/', configure.address_list, name='address_list', ),
    path('configure/address/<int:address_id>/edit/', configure.address_edit, name='address_edit', ),
    path('configure/address/<int:address_id>/delete/', configure.address_delete, name='address_delete', ),
    path('configure/subnet/create/', configure.subnet_create, name='subnet_create', ),
    path('configure/subnet/list/', configure.subnet_list, name='subnet_list', ),
    path('configure/subnet/<int:subnet_id>/edit/', configure.subnet_edit, name='subnet_edit', ),
    path('configure/subnet/<int:subnet_id>/delete/', configure.subnet_delete, name='subnet_delete', ),
]
