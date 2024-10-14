from django.db import models

from base.models import TimeStampedModel, UUIDModel


class ExportableModel(UUIDModel, TimeStampedModel):
    """
    Abstract Class for model exports

    EXPORT_RESOURCE needs to reference a ModelResource, otherwise a NotImplementedError is raised
    """

    from import_export.resources import ModelResource

    EXPORT_RESOURCE: ModelResource = None
    FILTER_FIELDS_MAP = {}

    export_file = models.FileField(null=True, blank=True)

    class StatusChoices(models.TextChoices):
        PROCESSING = "PROCESSING", "Processing"
        ERROR = "ERROR", "Error"
        FINISHED = "FINISHED", "Finished"

    status = models.TextField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PROCESSING)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    @property
    def EXPORT_MODEL(self):
        return self.EXPORT_RESOURCE._meta.model

    def save(self, *args, **kwargs):
        if self.EXPORT_RESOURCE is None:
            raise NotImplementedError(f"No EXPORT_RESOURCE set for {type(self).__name__}")

        if self.FILTER_FIELDS_MAP == {}:
            raise NotImplementedError(f"No FILTER_FIELDS_MAP set for {type(self).__name__}")

        for key, value in self.FILTER_FIELDS_MAP.items():
            field_1 = key.split("__")[0]
            field_2 = value.split("__")[0]
            if field_1 not in [field_1.name for field_1 in self.EXPORT_MODEL._meta.fields]:
                raise ValueError(
                    f"Field {field_1} is not a valid field for model {self.EXPORT_MODEL.__name__}. Check FILTER_FIELDS_MAP"
                )
            if field_2 not in [field_2.name for field_2 in self._meta.fields]:
                raise ValueError(
                    f"Field {field_2} is not a valid field for model {type(self).__name__}. Check FILTER_FIELDS_MAP"
                )

        created = self._state.adding
        instance = super().save(*args, **kwargs)
        if created or self.export_file.name == "":
            from apps.exports.tasks import save_export_file

            save_export_file.delay(self._meta.app_label, type(self).__name__, str(self.pk))

        return instance
