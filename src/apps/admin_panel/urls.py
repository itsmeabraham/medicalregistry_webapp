from django.urls import include, path

from .views import Index

app_name = "admin_panel"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("pacientes/", include("apps.admin_panel.modules.patients.urls")),
]

