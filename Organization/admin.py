from django.contrib import admin
from Organization.models import Organization, Department, OrganizationAddress, OrganizationSubnet

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(OrganizationAddress)
admin.site.register(OrganizationSubnet)
