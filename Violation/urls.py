from django.urls import path
from Violation import views

urlpatterns = [
    path('load/', views.violation_load, name='violation_load', ),
    path('create/', views.violation_create, name='violation_create', ),
    path('report/list/', views.violation_list, name='violation_list', ),
    path('<int:violation_id>/show/', views.violation_show, name='violation_show', ),
    path('violator/<int:violator_id>/show/', views.violator_show, name='violator_show', ),
]
