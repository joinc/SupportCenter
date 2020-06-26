"""SupportCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('profile/create', profile.profile_create, name='profile_create', ),
    path('profile/<int:profile_id>/show', profile.profile_show, name='profile_show', ),
    path('profile/<int:profile_id>/edit', profile.profile_edit, name='profile_edit', ),
    path('profile/<int:profile_id>/delete', profile.profile_delete, name='profile_delete', ),
    path('organization/list/', microservice.organization_all, name='organization_all', ),
    path('organization/list/<str:org_title>', microservice.organization_list, name='organization_list', ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
