from django.contrib import admin
from Violation.models import FileReport, Report, Violator, Incident, Violation

admin.site.register(FileReport)
admin.site.register(Report)
admin.site.register(Violator)
admin.site.register(Incident)
admin.site.register(Violation)
