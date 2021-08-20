from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path, include
# from Main import views, microservice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Main.urls')),
    path('contract/', include('Contract.urls')),
    path('organization/', include('Organization.urls')),
    path('profile/', include('Profile.urls')),
    path('signature/', include('Signature.urls')),
    path('violation/', include('Violation.urls', namespace='violation')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
