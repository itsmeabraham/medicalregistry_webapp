from import_export.fields import Field
from import_export.resources import ModelResource, RowResult
from import_export.widgets import ForeignKeyWidget, DateWidget, NumberWidget, TimeWidget


from apps.patients.models import Patient
from apps.doctors.models import Doctor
from .models import Appointment


class AppointmentResource(ModelResource):
    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super().import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            # Add a column with the error message
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result
    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "legacy_id",
            "date",
            "time",
            "motive",
            "note",
            "cabinet",
            "laboratories",
            "subjective",
            "objective",
            "analisis",
            "plan",
        ]
        import_id_fields = ['legacy_id',]
        skip_unchanged = True
        report_skipped = True
        raise_errors = False

    patient = Field(
        attribute="patient", column_name="Paciente ID",
        widget=ForeignKeyWidget(Patient, 'legacy_id'),
    )
    doctor = Field(
        attribute="doctor", column_name="Usuario Médico ID",
        widget=ForeignKeyWidget(Doctor, 'legacy_id'),
    )
    date = Field(
        attribute="date", column_name="Fecha Inicial",
        widget=DateWidget(format='%d/%m/%Y'), default=None
    )
    time = Field(
        attribute="time", column_name="Hora Inicial",
        widget=TimeWidget(format='%H:%M:%S'), default=None
    )
    motive = Field(attribute="motive", column_name="Motivo de Consulta")
    note = Field(attribute="note", column_name="Notas")
    cabinet = Field(attribute="cabinet", column_name="Gabinete")
    laboratories = Field(attribute="laboratories", column_name="Laboratorios")
    subjective = Field(attribute="subjective", column_name="Subjetivo")
    objective = Field(attribute="objective", column_name="Objetivo")
    analisis = Field(attribute="analisis", column_name="Analisis", default=None)
    plan = Field(attribute="plan", column_name="Plan", default=None)

