from django.urls import path
from Esign import views

urlpatterns = [
    path('', views.esign_list, name='esign_list', ),
    path('<int:esign_id>/show/', views.esign_show, name='esign_show', ),
    path('<int:esign_id>/terminate/', views.esign_terminate, name='esign_terminate', ),
    path('<int:esign_id>/delete/', views.esign_delete, name='esign_delete', ),
    path('upload/', views.esign_file_upload, name='esign_file_upload', ),
    path('<int:esign_id>/download/', views.esign_file_download, name='esign_file_download', ),
]