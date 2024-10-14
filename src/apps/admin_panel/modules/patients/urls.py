from django.urls import include, path

from .views import (
    Create, Delete, Detail, Index, List, Update,
)

app_name = "patients"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("listado/", List.as_view(), name="list"),
    path("crear/", Create.as_view(), name="create"),
    path(
        "<slug:patient_slug>/",
        include(
            [
                path("", Detail.as_view(), name="detail"),
                path("editar/", Update.as_view(), name="update"),
                path("eliminar/", Delete.as_view(), name="delete"),
            ]
        ),
    ),
]
