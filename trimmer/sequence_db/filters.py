from .models import *
import django_filters


class EntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    target = django_filters.CharFilter(field_name='metadata__target', lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = []
