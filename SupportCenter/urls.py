from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Main import views, microservice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index', ),
    path('login/', views.login, name='login', ),
    path('logout/', views.logout, name='logout', ),
    path('organization/', views.organization_list, name='organization_list', ),
    path('organization/<int:organization_id>/show/', views.organization_show, name='organization_show', ),
    path('organization/<int:organization_id>/edit/', views.organization_edit, name='organization_edit', ),
    path('organization/<int:organization_id>/delete/', views.organization_delete, name='organization_delete', ),
    path('profile/', include('Profile.urls')),
    path('esign/', include('Esign.urls')),

    # path('organization/list/', microservice.organization_all, name='organization_all', ),
    # path('organization/list/<str:org_title>', microservice.organization_list, name='organization_list', ),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
