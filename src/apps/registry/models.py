from django.db import models

from base.models import TimeStampedModel, UUIDModel
from django_ckeditor_5.fields import CKEditor5Field
from mptt.models import MPTTModel, TreeForeignKey
from admin_ordering.models import OrderableModel

# Create your models here.

class Registry(UUIDModel, TimeStampedModel):
    name = models.CharField('Nombre', max_length=128)

    def __str__(self):
        return self.name


class Section(MPTTModel, UUIDModel, TimeStampedModel):
    registry = models.ForeignKey('registry.Registry', on_delete=models.CASCADE)
    name = models.CharField('Nombre', max_length=128)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    variables = models.ManyToManyField('catalogs.Variable', through='registry.SectionVariable')
    

    def __str__(self):
        return self.name

class Flow(UUIDModel, TimeStampedModel):
    registry = models.ForeignKey('registry.Registry', on_delete=models.CASCADE)
    name = models.CharField('Nombre', max_length=128)
    start_section = models.ForeignKey(Section, on_delete=models.PROTECT)
    is_initial = models.BooleanField(default=True)
    is_subsecuent = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SectionVariable(UUIDModel, TimeStampedModel, OrderableModel):
    class Meta(OrderableModel.Meta):
        ...

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    variable = models.ForeignKey('catalogs.Variable', on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
