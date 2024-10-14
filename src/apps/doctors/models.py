from django.db import models

from base.models import TimeStampedModel, UUIDModel

# Create your models here.

class Organization(UUIDModel, TimeStampedModel):
    name = models.CharField('Nombre', max_length=128)


class Doctor(UUIDModel, TimeStampedModel):
    """
    Example. Johana
    """

    treatment = models.CharField(max_length=128, null=True, blank=True, default='Dr.')
    name = models.CharField(max_length=128, null=True, blank=True)
    father_last_name = models.CharField(max_length=128, null=True, blank=True)
    mother_last_name = models.CharField(max_length=128, null=True, blank=True)
    full_name = models.CharField(max_length=256, null=True, blank=True, editable=False)

    user = models.OneToOneField('users.User', on_delete=models.SET_NULL, null=True)
    organizations = models.ManyToManyField(Organization, )
    registries = models.ManyToManyField('registry.Registry', through='doctors.DoctorRegistry')


    def get_full_name(self):
        if any([self.name, self.father_last_name, self.mother_last_name]):
            return " ".join([
                self.treatment or '',
                self.name or '',
                self.father_last_name or '',
                self.mother_last_name or '',
            ])
        else:
            return f"Doctor Sin Nombre {self.pk}"

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or super().__str__()


class DoctorRegistry(UUIDModel, TimeStampedModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    registry = models.ForeignKey('registry.Registry', on_delete=models.CASCADE)
