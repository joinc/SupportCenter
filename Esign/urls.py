from django.urls import path
from Esign import views

urlpatterns = [
    path('', views.esign_get_list, name='esign_list', ),
    path('<int:esign_id>/show/', views.esign_show, name='esign_show', ),
    path('<int:esign_id>/download/', views.esign_download, name='esign_download', ),
    path('<int:esign_id>/terminate/', views.esign_terminate, name='esign_terminate', ),
]