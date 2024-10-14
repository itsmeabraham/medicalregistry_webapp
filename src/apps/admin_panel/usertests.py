from django.contrib.auth.mixins import UserPassesTestMixin


class AccessMixin:
    def test_func(self):
        is_active = self.request.user.is_active
        return is_active

