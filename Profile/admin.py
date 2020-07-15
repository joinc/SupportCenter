from django.contrib import admin
from Profile.models import UserProfile, AccessRole

admin.site.register(UserProfile)
admin.site.register(AccessRole)
