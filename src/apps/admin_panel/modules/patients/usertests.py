from apps.admin_panel.usertests import AccessMixin as Previous


class AccessMixin(Previous):
    def test_func(self):
        previous_conditions = super().test_func()
        return previous_conditions
