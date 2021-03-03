from django.urls import path
from Organization import views

urlpatterns = [
    path('list/', views.organization_list, name='organization_list', ),
    path('create/', views.organization_create, name='organization_create', ),
    path('<int:organization_id>/show/', views.organization_show, name='organization_show', ),
    path('<int:organization_id>/edit/', views.organization_edit, name='organization_edit', ),
    path('<int:organization_id>/delete/', views.organization_delete, name='organization_delete', ),
    path('address/<int:organization_id>/create/', views.organization_address_create, name='org_address_create', ),
    path('address/<int:org_address_id>/delete/', views.organization_address_delete, name='org_address_delete', ),
    path('subnet/<int:organization_id>/create/', views.organization_subnet_create, name='org_subnet_create', ),
    path('subnet/<int:org_subnet_id>/delete/', views.organization_subnet_delete, name='org_subnet_delete', ),
]
