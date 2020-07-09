from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='esign_index', ),
]