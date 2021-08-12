from django.urls import path
from Contract import views

urlpatterns = [
    path('list/', views.contract_list, name='contract_list', ),
    path('create/', views.contract_create, name='contract_create', ),
    path('<int:contract_id>/show/', views.contract_show, name='contract_show', ),
    path('<int:contract_id>/add_stage/', views.add_stage, name='add_stage', ),
    path('attache/<int:attache_id>/download/', views.attache_download, name='attache_download', ),
]
