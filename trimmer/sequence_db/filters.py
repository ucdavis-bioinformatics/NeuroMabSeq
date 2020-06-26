from .models import *
import django_filters

def get_mab_ids():
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    return lambda: sorted([(entry.mabid, entry.mabid) for entry in all_entries])

def get_targets():
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    return lambda: sorted(list(set([(entry.protein_target, entry.protein_target) for entry in all_entries
                           if entry.protein_target != 'nan' and entry.protein_target])))

def simple_get_targets():
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    return list(set([(entry.protein_target, entry.protein_target) for entry in all_entries
                           if entry.protein_target != 'nan' and entry.protein_target]))

def simple_get_mab_ids():
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    return sorted([(entry.mabid, entry.mabid) for entry in all_entries])

def get_categories():
    return [(i, categories[i]) for i in categories.keys()]

class EntryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    target = django_filters.CharFilter(field_name='metadata__target', lookup_expr='icontains')
    class Meta:
        model = Entry
        fields = []


class TrimmerEntryFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(field_name='mabid', lookup_expr='icontains')
    name_choice = django_filters.ChoiceFilter(field_name='mabid', choices=get_mab_ids())
    category_choice = django_filters.ChoiceFilter(field_name='category', choices=get_categories())
    target_choice = django_filters.ChoiceFilter(field_name='protein_target', choices=get_targets())
    ordering = django_filters.OrderingFilter(choices=(('mabid', 'MabID Ascending'), ('-mabid', 'MabID Descending'),
                                                      ('protein_target', 'Target Ascending'), ('-protein_target', 'Target Descending'),
                                                      ('category', 'Category Ascending'), ('-category', 'Category Descending'),
                                                      ('light_count', 'Light Count Ascending'), ('-light_count', 'Light Count Descending'),
                                                      ('heavy_count', 'Heavy Count Ascending'), ('-heavy_count', 'Heavy Count Descending')
                                                      ))
    search = django_filters.CharFilter()
    # search_target = django_filters.CharFilter()
    class Meta:
        model = TrimmerEntry
        fields = []
