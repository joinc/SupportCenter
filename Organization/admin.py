from django.contrib import admin
from Organization.models import Organization, Department, AddressOrg, SubnetOrg

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(AddressOrg)
admin.site.register(SubnetOrg)
