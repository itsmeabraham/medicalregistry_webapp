from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from import_export.resources import ModelResource


from .models import (
    Patient, Address, Phone
)
from apps.doctors.models import Doctor



class PatientResource(ModelResource):
    class Meta:
        model = Patient
        fields = [
            "id",
            "legacy_id",
            "doctor",
            "name",
            "father_last_name",
            "mother_last_name",
            "married_last_name",
            "date_of_birth",
            "gender",
            "email",
            "ocupation",
            "blood_type",
            "refered_by",
            "alergies",
            "comments",
            "alerts",
            "marital_status",
            "religion",
            "family_health_history",
            "personal_pathological_health_history",
            "personal_health_history",
            "gynecological_health_history",
        ]
        export_order = fields
        import_id_fields = ['legacy_id',]


    doctor = Field(
        attribute="doctor", column_name="Medico Tratante ID",
        widget=ForeignKeyWidget(Doctor, 'legacy_id')
    )
    name = Field(attribute="name", column_name="Nombres")
    father_last_name = Field(attribute="father_last_name", column_name="Apellido Paterno")
    mother_last_name = Field(attribute="mother_last_name", column_name="Apellido Materno")
    married_last_name = Field(attribute="married_last_name", column_name="Apellido Casada")
    date_of_birth = Field(attribute="date_of_birth", column_name="Fecha de Nacimiento")
    gender = Field(attribute="gender", column_name="Sexo")
    email = Field(attribute="email", column_name="Correo Electrónico")
    ocupation = Field(attribute="ocupation", column_name="Ocupación")
    blood_type = Field(attribute="blood_type", column_name="Tipo de Sangre")
    refered_by = Field(attribute="refered_by", column_name="Referido Por")
    alergies = Field(attribute="alergies", column_name="Alergias")
    comments = Field(attribute="comments", column_name="Comentarios")
    alerts = Field(attribute="alerts", column_name="Alertas")
    marital_status = Field(attribute="marital_status", column_name="Estado Civil")
    religion = Field(attribute="religion", column_name="Religión")
    family_health_history = Field(attribute="family_health_history", column_name="Antecedentes Heredo Familiares Texto Libre")
    personal_health_history = Field(attribute="personal_health_history", column_name="Antecedentes Personales No Patológicos Texto Libre")
    personal_pathological_health_history = Field(attribute="personal_pathological_health_history", column_name="Antecedentes Personales Patológicos Texto Libre")
    gynecological_health_history = Field(attribute="gynecological_health_history", column_name="Antecedentes Gineco Obstetricos Texto Libre")


class AddressResource(ModelResource):
    class Meta:
        model = Address
        fields = [
            "id",
            "patient",
            "street",
            "neighborhood",
            "county",
            "state",
            "zip_code",
        ]
        import_id_fields = ('id',)
    patient = Field(
        attribute="patient", column_name="Paciente ID",
        widget=ForeignKeyWidget(Patient, 'legacy_id'),
    )
    street = Field(attribute="street", column_name="Dirección")
    neighborhood = Field(attribute="neighborhood", column_name="Colonia")
    county = Field(attribute="county", column_name="Delg./Mpio.")
    state = Field(attribute="state", column_name="Estado")
    zip_code = Field(attribute="zip_code", column_name="CP")
    country = Field(attribute="country", column_name="País")


class PhoneResource(ModelResource):
    class Meta:
        model = Phone
        fields = [
            "id",
            "patient",
            "number",
            "type_of",
        ]
        import_id_fields = ('id',)
    patient = Field(
        attribute="patient", column_name="Paciente ID",
        widget=ForeignKeyWidget(Patient, 'legacy_id'),
    )
    number = Field(attribute="number", column_name="Numero")
    type_of = Field(attribute="type_of", column_name="Tipo")


