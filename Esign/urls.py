from django.urls import path
from . import views

urlpatterns = [
    path('', views.esign_list, name='esign_list', ),
]