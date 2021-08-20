from django.urls import path
from Violation import views

app_name = 'violation'

urlpatterns = [
    path('load/', views.report_load, name='report_load', ),
    path('report/list/', views.report_list, name='report_list', ),
    path('report/<int:report_id>/show/', views.report_show, name='report_show', ),
    path('<int:violation_id>/show/', views.violation_show, name='violation_show', ),
]
