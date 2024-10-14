from django.db import models
from base.models import UUIDModel, TimeStampedModel
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.functional import cached_property
import datetime


# Create your models here.



class Evaluation(UUIDModel, TimeStampedModel):
    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['-date', '-time']


    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, verbose_name="paciente", related_name="appointments")
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.PROTECT, verbose_name="doctor", null=True)

    date = models.DateField('Fecha',)
    time = models.TimeField('Hora', null=True, blank=True)






    def __str__(self):
        return f"{self.patient} - {self.date.strftime('%d/%b/%y')}"
        #return super().__str__()






