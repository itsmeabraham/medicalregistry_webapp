from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Patient
)




@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    ...

