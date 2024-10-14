from django.db import models
from base.models import TimeStampedModel, UUIDModel
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.functional import cached_property


# Create your models here.


class Patient(UUIDModel, TimeStampedModel):
    """
    Example. Johana
    """

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    class GenderChoices(models.TextChoices):
        MALE = 'H', "Hombre"
        FEMALE = 'M', "Mujer"
        OTHER = 'O', "Otro"

    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.PROTECT, verbose_name="Médico Tratante", null=True, blank=True)
    organization = models.ForeignKey('doctors.Organization', on_delete=models.PROTECT, verbose_name="Organizacion", null=True, blank=True)

    file_number = models.CharField('Numero de Expediente', max_length=128, null=True, blank=True)
    name = models.CharField('Nombre', max_length=128, null=True, blank=True)
    father_last_name = models.CharField('Apellido Paterno', max_length=128, null=True, blank=True)
    mother_last_name = models.CharField('Apellido Materno', max_length=128, null=True, blank=True)
    married_last_name = models.CharField('Apellido de Casada', max_length=128, null=True, blank=True)
    full_name = models.CharField(max_length=256, null=True, blank=True, editable=False)

    date_of_birth = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    gender = models.CharField(max_length=128, null=True, blank=True, choices=GenderChoices.choices)


    email = models.EmailField(null=True, blank=True)




    def get_full_name(self):
        if any([self.name, self.father_last_name, self.mother_last_name]):
            return " ".join([
                self.name or '',
                self.father_last_name or '',
                self.mother_last_name or '',
                f"({self.married_last_name})" if self.married_last_name else ''
            ])
        else:
            return f"Paciente Sin Nombre {self.pk}"

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or super().__str__()


