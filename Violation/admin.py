from django.contrib import admin
from Violation.models import FileViolation, ReportViolation, Violator, Incident

admin.site.register(FileViolation)
admin.site.register(ReportViolation)
admin.site.register(Violator)
admin.site.register(Incident)
