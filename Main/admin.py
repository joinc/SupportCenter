from django.contrib import admin
from Main.models import Organization, UserProfile, AccessRole

admin.site.register(Organization)
admin.site.register(AccessRole)
admin.site.register(UserProfile)
