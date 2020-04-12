from .models import *
import django_filters

def get_mab_ids():
    return lambda: [(entry.mabid, entry.mabid) for entry in TrimmerEntry.objects.all()]


class EntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    target = django_filters.CharFilter(field_name='metadata__target', lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = []


class TrimmerEntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='mabid', lookup_expr='icontains')
    name_choice = django_filters.MultipleChoiceFilter(field_name='mabid', choices=get_mab_ids())
    class Meta:
        model = TrimmerEntry
        fields = []
