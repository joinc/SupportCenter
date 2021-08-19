from django.urls import path
from Violation import views

urlpatterns = [
    path('load/', views.report_load, name='report_load', ),
    path('report/list/', views.report_list, name='report_list', ),
    path('report/<int:report_id>/show/', views.report_show, name='report_show', ),
    path('report/<int:report_id>/violator/<int:violator_id>/show/', views.violator_show, name='violator_show', ),
]
