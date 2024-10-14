from django.contrib import admin
from .models import Doctor, Organization, DoctorRegistry

# Register your models here.


class DoctorRegistryInline(admin.TabularInline):
    model = DoctorRegistry

admin.site.register(Organization)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    inlines = [DoctorRegistryInline]
