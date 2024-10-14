from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from admin_ordering.admin import OrderableAdmin

from .models import Registry, Section, Flow, SectionVariable


# Register your models here.


admin.site.register(Registry)
admin.site.register(Flow)


class SectionVariableInline(OrderableAdmin, admin.TabularInline):
    model = SectionVariable
    fields = [
        'ordering',
        'section', 'variable', 'is_required',
    ]
    ordering_field = "ordering"
    ordering_field_hide_input = True


@admin.register(Section)
class SectionAdmin(DraggableMPTTAdmin):
    inlines = [SectionVariableInline]


