from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import (
    Variable, ChoiceVariable, ChoiceOption,
    FileVariable, NumberVariable, TextVariable
)

@admin.register(Variable)
class Variable(PolymorphicParentModelAdmin):
    base_model = Variable
    child_models = [
        ChoiceVariable, FileVariable, NumberVariable,
        TextVariable
    ]

class ChoiceOptionInline(admin.TabularInline):
    model = ChoiceOption

@admin.register(ChoiceVariable)
class ChoiceVariableAdmin(PolymorphicChildModelAdmin):
    base_model = ChoiceVariable
    inlines = [ChoiceOptionInline]

@admin.register(FileVariable)
class FileVariableAdmin(PolymorphicChildModelAdmin):
    base_model = FileVariable

@admin.register(NumberVariable)
class NumberVariableAdmin(PolymorphicChildModelAdmin):
    base_model = NumberVariable

@admin.register(TextVariable)
class TextVariableAdmin(PolymorphicChildModelAdmin):
    base_model = TextVariable
