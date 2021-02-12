from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.organization_list, name='organization_list', ),
    path('create/', views.organization_create, name='organization_create', ),
    path('<int:organization_id>/show/', views.organization_show, name='organization_show', ),
    path('<int:organization_id>/edit/', views.organization_edit, name='organization_edit', ),
    path('<int:organization_id>/delete/', views.organization_delete, name='organization_delete', ),

]