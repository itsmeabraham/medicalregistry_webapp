from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



from .usertests import AccessMixin



class Index(LoginRequiredMixin, TemplateView):
    template_name = "admin_panel/index.html"


