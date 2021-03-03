from django.contrib import admin
from Profile.models import Permission, PresetAccess, UserProfile, Access

admin.site.register(Permission)
admin.site.register(PresetAccess)
admin.site.register(UserProfile)
admin.site.register(Access)
