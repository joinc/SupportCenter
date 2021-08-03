from django.urls import path
from Contract import views

urlpatterns = [
    path('list/', views.contract_list, name='contract_list', ),
    path('create/', views.contract_create, name='contract_create', ),
    path('<int:contract_id>/show/', views.contract_show, name='contract_show', ),
    # path('<int:organization_id>/edit/', views.organization_edit, name='organization_edit', ),
    # path('<int:organization_id>/delete/', views.organization_delete, name='organization_delete', ),
    # path('address/<int:organization_id>/create/', views.organization_address_create, name='org_address_create', ),
    # path('address/<int:org_address_id>/delete/', views.organization_address_delete, name='org_address_delete', ),
    # path('subnet/<int:organization_id>/create/', views.organization_subnet_create, name='org_subnet_create', ),
    # path('subnet/<int:org_subnet_id>/delete/', views.organization_subnet_delete, name='org_subnet_delete', ),
]
