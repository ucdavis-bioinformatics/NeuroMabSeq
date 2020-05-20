from .models import *
import django_filters

def get_mab_ids():
    return lambda: sorted([(entry.mabid, entry.mabid) for entry in TrimmerEntry.objects.filter(show_on_web=True)])

def get_targets():
    return lambda: sorted(list(set([(entry.protein_target, entry.protein_target) for entry in TrimmerEntry.objects.filter(show_on_web=True)
                           if entry.protein_target != 'nan' and entry.protein_target])))

def get_categories():
    return [(i, categories[i]) for i in categories.keys()]

class EntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    target = django_filters.CharFilter(field_name='metadata__target', lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = []


class TrimmerEntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='mabid', lookup_expr='icontains')
    name_choice = django_filters.MultipleChoiceFilter(field_name='mabid', choices=get_mab_ids())
    category_choice = django_filters.MultipleChoiceFilter(field_name='category', choices=get_categories())
    target_choice = django_filters.MultipleChoiceFilter(field_name='protein_target', choices=get_targets())
    class Meta:
        model = TrimmerEntry
        fields = []
