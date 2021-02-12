from django.contrib import admin
from Violation.models import ReportViolation, Violator, Incident

admin.site.register(ReportViolation)
admin.site.register(Violator)
admin.site.register(Incident)
