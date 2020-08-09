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

def get_failures():
    all_entries = TrimmerEntryStatus.objects.filter()
    return lambda: sorted(list(set([(entry.failure, entry.failure) for entry in all_entries])))

def get_volume():
    all_entries = TrimmerEntryStatus.objects.filter()
    return lambda: sorted(list(set([(entry.volume, entry.volume) for entry in all_entries])))

def get_concentration():
    all_entries = TrimmerEntryStatus.objects.filter()
    return lambda: sorted(list(set([(entry.concentration, entry.concentration) for entry in all_entries])))

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

# class EntryFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
#     target = django_filters.CharFilter(field_name='metadata__target', lookup_expr='icontains')
#     class Meta:
#         model = Entry
#         fields = []


class TrimmerSequenceFilter(django_filters.FilterSet):
    mabid_search = django_filters.CharFilter(field_name='entry__mabid', lookup_expr='icontains')
    mabid = django_filters.ChoiceFilter(field_name='entry__mabid', choices=get_mab_ids())
    category = django_filters.ChoiceFilter(field_name='entry__category', choices=get_categories())
    target = django_filters.ChoiceFilter(field_name='entry__protein_target', choices=get_targets())
    chain = django_filters.ChoiceFilter(field_name='chain', choices=(("Light", "Light"),("Heavy", "Heavy")))
    ordering = django_filters.OrderingFilter(choices=(('entry__mabid', 'MabID Ascending'), ('-entry__mabid', 'MabID Descending'),
                                                      ('entry__protein_target', 'Target Ascending'), ('-entry__protein_target', 'Target Descending'),
                                                      ('entry__category', 'Category Ascending'), ('-entry__category', 'Category Descending'),
                                                      # ('light_count', 'Light Count Ascending'), ('-light_count', 'Light Count Descending'),
                                                      # ('heavy_count', 'Heavy Count Ascending'), ('-heavy_count', 'Heavy Count Descending')
                                                      ))
    search = django_filters.CharFilter()
    # search_target = django_filters.CharFilter()
    class Meta:
        model = TrimmerEntry
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





class TrimmerStatusFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(field_name='mabid', lookup_expr='icontains')
    # name_choice = django_filters.ChoiceFilter(field_name='mabid', choices=get_mab_ids())
    sample_name = django_filters.CharFilter(field_name='plate_name', lookup_expr='icontains')
    plate_location = django_filters.CharFilter(field_name='plate_location', lookup_expr='icontains')
    failure = django_filters.ChoiceFilter(field_name='failure', choices=get_failures())
    concentration = django_filters.ChoiceFilter(field_name='concentration', choices=get_concentration())
    volume = django_filters.ChoiceFilter(field_name='volume', choices=get_volume())
    # sample_name = django_filters.CharFilter(field_name='plate_name', lookup_expr='icontains')
    # sample_name = django_filters.CharFilter(field_name='plate_name', lookup_expr='icontains')
    ordering = django_filters.OrderingFilter(choices=(('entry', 'Entry Ascending'), ('-entry', 'MabID Descending'),
                                                      ('sample_name', 'Sample Name Ascending'), ('-sample_name', 'Sample Name Descending'),
                                                      ('plate_location', 'Plate Location Ascending'), ('-sample_name', 'Plate Location Descending'),
                                                      ('volume', 'Volume Ascending'), ('-volume', 'Volume Descending'),
                                                      ('concentration', 'Concentration Ascending'), ('-concentration', 'Concentration Descending'),
                                                      ('LCs_reported', 'Light Count Ascending'), ('-LCs_reported', 'Light Count Descending'),
                                                      ('HCs_repoted', 'Heavy Count Ascending'), ('-HCs_reported', 'Heavy Count Descending')
                                                      ))

    search = django_filters.CharFilter()
    class Meta:
        model = TrimmerEntryStatus
        fields = []
