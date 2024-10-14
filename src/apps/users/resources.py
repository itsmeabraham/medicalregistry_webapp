from import_export.resources import ModelResource

from .models import User


class UserResource(ModelResource):
    class Meta:
        model = User
        fields = ["uuid", "email"]
