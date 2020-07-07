from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Main import views, profile, microservice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index', ),
    path('login/', views.login, name='login', ),
    path('logout/', views.logout, name='logout', ),
    path('profile/list', profile.profile_list, name='profile_list', ),
    path('profile/<int:profile_id>/show', profile.profile_show, name='profile_show', ),
    path('profile/<int:profile_id>/edit', profile.profile_edit, name='profile_edit', ),
    path('organization/list/', microservice.organization_all, name='organization_all', ),
    path('organization/list/<str:org_title>', microservice.organization_list, name='organization_list', ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
