from rest_framework.permissions import AllowAny
from django.contrib.auth import get_permission_codename
from django.contrib.auth.mixins import PermissionRequiredMixin


class PublicMixin:
    permission_classes = [AllowAny]

    @property
    def model(self):
        """
        Retrieve model used in serializer
        """
        return self.serializer_class.Meta.model

    def get_queryset(self):
        """
        Get objects
        """
        if self.queryset:
            return self.queryset
        return self.model.objects.all()







class PermsView(PermissionRequiredMixin):
    def has_permission(self):
        opts = self.model._meta
        codename = get_permission_codename("view", opts)
        return self.request.user.has_perm("%s.%s" % (opts.app_label, codename))


class PermsChange(PermissionRequiredMixin):
    def has_permission(self):
        opts = self.model._meta
        codename = get_permission_codename("change", opts)
        return self.request.user.has_perm("%s.%s" % (opts.app_label, codename))


class PermsAdd(PermissionRequiredMixin):
    def has_permission(self):
        opts = self.model._meta
        codename = get_permission_codename("add", opts)
        return self.request.user.has_perm("%s.%s" % (opts.app_label, codename))


class PermsDelete(PermissionRequiredMixin):
    def has_permission(self):
        opts = self.model._meta
        codename = get_permission_codename("delete", opts)
        return self.request.user.has_perm("%s.%s" % (opts.app_label, codename))
