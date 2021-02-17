from django.contrib import admin
from Profile.models import CategoryPermission, Permission, AccessRole, PresetAccess, UserProfile, Access

admin.site.register(CategoryPermission)
admin.site.register(Permission)
admin.site.register(AccessRole)
admin.site.register(PresetAccess)
admin.site.register(UserProfile)
admin.site.register(Access)
