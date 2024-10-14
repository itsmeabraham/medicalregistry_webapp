from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)
from django_filters.views import FilterView

from apps.patients.models import (
    Patient as MODEL

)
from apps.users.mixins import PermsAdd, PermsChange, PermsDelete, PermsView

from .forms import (
    CreateForm, UpdateForm
)
from .usertests import AccessMixin
from .filters import PatientFilter

TEMPLATE_ROOT = "admin_panel/patients/"
SLUG_URL_KWARG = 'patient_slug'
SLUG_FIELD = 'uuid'


class BaseView(AccessMixin):
    model = MODEL
    slug_url_kwarg = SLUG_URL_KWARG
    slug_field = SLUG_FIELD

    def get_patient(self):
        patient = Model.objects.get(uuid=self.kwargs.get('patient_slug'))
        return patient


class Index(BaseView, FilterView, PermsView, ListView):
    template_name = TEMPLATE_ROOT + "index.html"
    filterset_class = PatientFilter
    paginate_by = 100



class List(BaseView, PermsView, ListView):
    template_name = TEMPLATE_ROOT + "list.html"


class Create(BaseView, PermsAdd, CreateView):
    template_name = TEMPLATE_ROOT + "create.html"
    form_class = CreateForm

    def get_success_url(self, *args, **kwargs):
        self.kwargs[SLUG_URL_KWARG] = getattr(self.object, SLUG_FIELD)
        return reverse("admin_panel:patients:detail", kwargs=self.kwargs)


class Detail(BaseView, PermsView, DetailView):
    template_name = TEMPLATE_ROOT + "detail.html"


class Update(BaseView, PermsChange, UpdateView):
    template_name = TEMPLATE_ROOT + "update.html"
    form_class = UpdateForm

    def get_success_url(self, *args, **kwargs):
        return reverse("admin_panel:patients:detail", kwargs=self.kwargs)


class Delete(BaseView, PermsDelete, DeleteView):
    template_name = TEMPLATE_ROOT + "delete.html"

    def get_success_url(self, *args, **kwargs):
        self.kwargs.pop(SLUG_URL_KWARG)
        return reverse("admin_panel:patients:index", kwargs=self.kwargs)





