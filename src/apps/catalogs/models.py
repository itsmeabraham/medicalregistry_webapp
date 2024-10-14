from django.db import models

from base.models import TimeStampedModel, UUIDModel
from django_ckeditor_5.fields import CKEditor5Field
from polymorphic.models import PolymorphicModel


# Create your models here.


class Variable(PolymorphicModel, UUIDModel, TimeStampedModel):
    class Meta():
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    name = models.CharField('Nombre', max_length=128)

    def __str__(self):
        return self.name


class ChoiceVariable(Variable):
    class TypeChoices(models.TextChoices):
        SINGLE = "SINGLE", "Seleccion Unica"
        MULTIPLE = "MULTIPLE", "Seleccion Multiple"
    type_of = models.CharField(
        'Tipo de Seleccion', max_length=16, null=True, blank=True, 
        choices=TypeChoices.choices, default=TypeChoices.SINGLE
    )

class ChoiceOption(UUIDModel, TimeStampedModel):
    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'

    choice_variable = models.ForeignKey(ChoiceVariable, on_delete=models.CASCADE)
    name = models.CharField('Nombre', max_length=128, null=True, blank=True)

class FileVariable(Variable):
    ...

class NumberVariable(Variable):
    max_limit = models.CharField('Maximo', max_length=128, null=True, blank=True)
    min_limit = models.CharField('Minimo', max_length=128, null=True, blank=True)
    decima_places = models.PositiveSmallIntegerField(default=0)
    unit = models.CharField('Unidad', max_length=128, null=True, blank=True)


class TextVariable(Variable):
    class DisplayChoices(models.TextChoices):
        SINGLE = "SINGLE", "Una Linea"
        MULTIPLE = "MULTIPLE", "Muchas Lineas"

    display = models.CharField(
        'Tipo de Vista', max_length=128, null=True, blank=True, 
        choices=DisplayChoices.choices, default=DisplayChoices.SINGLE
    )
