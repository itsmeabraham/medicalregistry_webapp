from django import forms

from apps.patients.models import (
    Patient as MODEL,
)


class CreateForm(forms.ModelForm):
    class Meta:
        model = MODEL
        fields = [
            "name",
            "father_last_name",
            "mother_last_name",
            "married_last_name",
            "date_of_birth",
            "email",
            "doctor",
        ]


class UpdateForm(CreateForm):
    pass



