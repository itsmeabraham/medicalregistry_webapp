from django.contrib import admin


class ExportableModelAdmin(admin.ModelAdmin):
    list_display = ["created_at", "export_file", "status"]
    readonly_fields = ["export_file", "status"]
