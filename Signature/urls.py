from django.urls import path
from Signature import views

urlpatterns = [
    path('list/', views.signature_list, name='signature_list', ),
    path('upload/', views.signature_file_upload, name='signature_file_upload', ),
    path('<int:signature_id>/show/', views.signature_show, name='signature_show', ),
    path('<int:signature_id>/terminate/', views.esign_terminate, name='signature_terminate', ),
    path('<int:signature_id>/delete/', views.esign_delete, name='signature_delete', ),
    path('<int:signature_id>/download/', views.esign_file_download, name='signature_file_download', ),
]