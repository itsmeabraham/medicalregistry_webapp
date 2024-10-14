import django_filters
from apps.patients.models import Patient
from django.db.models import Q




class PatientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='name', label='Nombre')
    last_names = django_filters.CharFilter(label='Apellidos', method='both_last_names')
    class Meta:
        model = Patient
        fields = ['name', 'last_names']


    def both_last_names(self, queryset, name, value):
        return queryset.filter(Q(father_last_name__icontains=value) | Q(mother_last_name__icontains=value))

