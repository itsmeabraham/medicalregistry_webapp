from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.core.files.base import ContentFile
from django.db.models import Model
from import_export.resources import ModelResource

from services.pusher import PusherClient

from .models import ExportableModel

logger = get_task_logger(__name__)


@shared_task
def save_export_file(app_label: str, model_name: str, uuid: str):
    logger.info(f"Celery received {app_label}.{model_name} with PK {uuid} for processing export")
    ModelExportClass: ExportableModel = apps.get_model(app_label, model_name)
    try:
        model_export_instance: ExportableModel = ModelExportClass.objects.get(pk=uuid)
    except ModelExportClass.DoesNotExist as e:
        raise e
    ResourceClass: ModelResource = model_export_instance.EXPORT_RESOURCE
    ModelClass: Model = model_export_instance.EXPORT_MODEL

    filters = {
        key: getattr(model_export_instance, value, None)
        for key, value in model_export_instance.FILTER_FIELDS_MAP.items()
        if getattr(model_export_instance, value, None) is not None
    }

    queryset = ModelClass.objects.filter(**filters)

    dataset = ResourceClass().export(queryset=queryset)

    csv_file = ContentFile(dataset.export("csv"))

    model_export_instance.export_file.save(f"{model_export_instance.EXPORT_MODEL.__name__}.csv", csv_file)

    model_export_instance.status = model_export_instance.StatusChoices.FINISHED

    model_export_instance.save()

    pusher = PusherClient()

    pusher.trigger("exports", "export-finished", {"uuid": str(model_export_instance.pk)})
