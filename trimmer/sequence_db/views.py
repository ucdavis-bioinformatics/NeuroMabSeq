from django.template import loader
from .models import *
from django.views.generic import DetailView
from .filters import *
from .forms import *
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
from .methods import *
from django.shortcuts import render, redirect
from django.conf import settings
import urllib
import json
import plotly.express as px
from django.views.generic import View
import csv
from Bio import SearchIO
import random
import string

# API STUFF
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters



def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# TODO fix this so to filter pos and neg from Light and Heavy
def main_page(request):
    html = 'home.html'
    context = {}
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    context['number_entries'] = len(all_entries)
    context['number_light'] = len(TrimmerLight.objects.filter(duplicate=False, entry__show_on_web=True))
    context['number_heavy'] = len(TrimmerHeavy.objects.filter(duplicate=False, entry__show_on_web=True))
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))


def GetAsvGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[float(i) for i in df_l['asv_support'] if i is not None], [float(i) for i in df_h['asv_support'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = px.box()
    figure.add_trace(go.Box(y=values[0], quartilemethod="inclusive", name="Light Chain ASV Count"))
    figure.add_trace(go.Box(y=values[1], quartilemethod="inclusive", name="Heavy Chain ASV Count"))
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetPctGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[float(i) for i in df_l['pct_support'] if i is not None], [float(i) for i in df_h['pct_support'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = px.box()
    figure.add_trace(go.Box(y=values[0], quartilemethod="inclusive", name="Light Chain Percent Support"))
    figure.add_trace(go.Box(y=values[1], quartilemethod="inclusive", name="Heavy Chain Percent Support"))
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div



def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)

def blat(request):
    context = {}
    context['queryset'] = None
    if request.method == 'POST':
        form = Blat(request.POST)
        if form.is_valid():
            # Get the From Data

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            sequence = form.cleaned_data['sequence']
            type = form.cleaned_data['type']
            context['form'] = Blat(initial={"sequence": sequence, "type":type})
            if not result['success']:
                return render(request, 'blat.html', context)

            # Create  some temp files (query file .fa and psl) for running BLAT
            rand_string = get_random_string(10)
            file_name = '../static_data/%s.fa' % rand_string
            with open(file_name, 'w') as temp_file:
                temp_file.write('>%s' % rand_string + '\n')
                temp_file.write(sequence)
            psl = '../static_data/%s.psl' % rand_string

            # Run BLAT
            call = 'blat ../static_data/%s.fa %s -t=%s -q=%s %s' % (type, file_name, type, type, psl)
            os.popen(call).read()

            # Core BLAT result processing
            try:
                qresult = SearchIO.read(psl, 'blat-psl')
            except:
                qresult = None
            all_results = []
            if qresult:
                for i in qresult:
                    temp_dict = dict(**i._items[0].__dict__, **i._items[0]._items[0].__dict__)
                    parse_id = temp_dict['_hit_id'].replace(':'," ").split('_')
                    temp_dict['mabid'] = parse_id[1]
                    temp_dict['pk'] = parse_id[0]
                    temp_dict['chain'] = parse_id[-2]
                    all_results.append(temp_dict)


            context['queryset'] = list(sorted(all_results, key=lambda d: (d['score'], d['ident_pct']), reverse=True))
            os.system('rm %s %s' % (file_name, psl))
            return render(request, 'blat.html', context)
    else:
        context['form'] = Blat()
    return render(request, 'blat.html', context)

#
# def GetScoreGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[float(i) for i in df_l['score'] if i is not None], [float(i) for i in df_h['score'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Score for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def GetSeqGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[len(i) for i in df_l['seq'] if i is not None], [len(i) for i in df_h['seq'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Sequence Length for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def GetAAGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[len(i) for i in df_l['aa'] if i is not None], [len(i) for i in df_h['aa'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Amino Acid Length for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def GetDomainGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[len(i) for i in df_l['aa'] if i is not None], [len(i) for i in df_h['domain'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Coding Domain Length for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def GetSeqStopGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#
#     df_l = df_l.replace([np.inf, -np.inf], np.nan).dropna(how="all")
#     df_h = df_h.replace([np.inf, -np.inf], np.nan).dropna(how="all")
#
#     values = [[i for i in df_l['seq_stop_index'] if i is not None], [i for i in df_h['seq_start_index'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Sequence Stop Index for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def GetSeqStartGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#
#     df_l = df_l.replace([np.inf, -np.inf], np.nan).dropna(how="all")
#     df_h = df_h.replace([np.inf, -np.inf], np.nan).dropna(how="all")
#
#     values = [[i for i in df_l['seq_start_index'] if i is not None], [i for i in df_h['seq_start_index'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Sequence Start Index for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div
#
#
# def ScoreGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[len(i) for i in df_l['score_index'] if i is not None], [len(i) for i in df_h['score_index'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = ff.create_distplot(values, group_labels, bin_size=1, show_hist=False)
#     figure.update_layout(title_text='Distribution of Sequence Length for Heavy Chain vs Light Chain')
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div

def faq_view(request):
    context = {}
    return render(request, 'faq.html', context)


def analytics_view(request):
    context = {}
    context['graph'] = GetAsvGraph()
    context['graph_pct'] = GetPctGraph()
    # context['graph_seq'] = GetSeqGraph()
    #context['graph_aa'] = GetAAGraph()
    #context['graph_domain'] = GetDomainGraph()
    #context['graph_seq_start'] = GetSeqStartGraph()
    #context['graph_seq_stop'] = GetSeqStopGraph()
    #context['graph_score'] = GetScoreGraph()
    return render(request, 'analytics.html', context)


class EntryDetailView(DetailView):
    model = Entry
    template_name = 'entry.html'

    def get_object(self, *args, **kwargs):
        obj = super(EntryDetailView, self).get_object(*args, **kwargs)
        return obj

    def get_context_data(self, **kwargs):
        # make sure that the invoices are not too many for the view but are still graphed
        context = super().get_context_data(**kwargs)
        context['entry'] = Entry.objects.get(pk=self.kwargs['pk'])
        return context


class TrimmerEntryDetailView(DetailView):
    model = TrimmerEntry
    template_name = 'new_entry.html'

    def get_object(self, *args, **kwargs):
        obj = super(TrimmerEntryDetailView, self).get_object(*args, **kwargs)
        return obj

    def get_context_data(self, **kwargs):
        # make sure that the invoices are not too many for the view but are still graphed
        context = super().get_context_data(**kwargs)
        context['entry'] = TrimmerEntry.objects.get(pk=self.kwargs['pk'])
        context['light'] = TrimmerLight.objects.filter(entry=context['entry'], duplicate=False).order_by('-asv_support')
        # context['light_duplicates'] = TrimmerLight.objects.filter(entry=context['entry'], duplicate=True)
        context['heavy'] = TrimmerHeavy.objects.filter(entry=context['entry'], duplicate=False).order_by('-asv_support')
        # context['heavy_duplicates'] = TrimmerHeavy.objects.filter(entry=context['entry'], duplicate=True)
        #context['graph'] = GetAsvGraph()
        #context['graph_pct'] = GetPctGraph()
        #context['graph_seq'] = GetSeqGraph()

        #context['graph_h'] = GetHeavyAsvGraph()
        return context


def TrimmerEntryListView(request):
    context = {}

    context['protein_targets'] = [i[0] for i in simple_get_targets()]
    context['mabids'] = [i[0] for i in simple_get_mab_ids()]
    context['categories'] = [i[0] for i in simple_get_mab_ids()]
    all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    context['filter'] = TrimmerEntryFilter(request.GET, queryset=all_entries)
    # context['queryset'] = context['filter'].qs.order_by(F('category').asc(nulls_last=True))
    return render(request, 'new_query.html', context)





def TrimmerStatusListView(request):
    context = {}

    #context['all_entries'] = TrimmerEntryStatus.objects.all()
    #context['status_entries'] = [i.entry.mabid for i in TrimmerEntryStatus.objects.all()]

    #context['entries'] = [i.mabid for i in TrimmerEntry.objects.all()]

    #context['status_not_in_entries'] = status_not_present()
    #context['entries_not_in_status'] = sorted(list(set(context['entries']) - set(context['status_entries'])))

    #context['messages'] = Messages.objects.all()
    #context['messages'] = [i.message.split(':')[1].replace(' ', '') for i in context['messages'] if 'metadata' in i.message]
    #

    #context['metadata_minus_status'] = sorted(list(set(context['messages']) - set(context['status_entries'])))
    #context['status_minus_metadata'] = sorted(list(set(context['status_entries']) - set(context['messages'])))
    context['protein_targets'] = [i[0] for i in simple_get_targets()]
    context['mabids'] = [i[0] for i in simple_get_mab_ids()]
    context['categories'] = [i[0] for i in simple_get_mab_ids()]
    all_entries = TrimmerEntryStatus.objects.filter(entry__show_on_web=True, )

    context['filter'] = TrimmerStatusFilter(request.GET, queryset=all_entries)

    # TODO plate stats for this view
    context['plate_stats'] = ''
    return render(request, 'status_list.html', context)


# def EntryListView(request):
#     context = {}
#     all_entries = Entry.objects.all()
#     context['filter'] = EntryFilter(request.GET, queryset=all_entries)
#     context['queryset'] = context['filter'].qs.order_by('-name')
#     return render(request, 'query.html', context)


# class EntryViewSet(viewsets.ModelViewSet):
#     serializer_class = TrimmerEntrySerializer
#
#     def get_queryset(self):
#         context = super(EntryViewSet, self).get_serializer_context()
#         all_entries = TrimmerEntry.objects.filter(show_on_web=True, )
#         all_entries = all_entries.exclude(mabid__contains='positive')
#         all_entries = all_entries.exclude(mabid__contains='negative')
#         return all_entries
#
#     def get_serializer_context(self):
#         context = super(EntryViewSet, self).get_serializer_context()
#         context.update({"request": self.request})
#         return context


class APIEntryListView(generics.ListAPIView):
    queryset = TrimmerEntry.objects.filter(show_on_web=True, )
    queryset = queryset.exclude(mabid__contains='positive')
    queryset = queryset.exclude(mabid__contains='negative')
    serializer_class = TrimmerEntrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['mabid', 'category', 'protein_target']
    search_fields = ['mabid', 'protein_target']
    ordering_fields = '__all__'


# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'
#     max_page_size = 50000

class APIStatusListView(generics.ListAPIView):
    queryset = TrimmerEntryStatus.objects.filter(entry__show_on_web=True, )
    # queryset = queryset.exclude(mabid__contains='positive')
    # queryset = queryset.exclude(mabid__contains='negative')
    serializer_class = TrimmerStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # pagination_class = LargeResultsSetPagination
    # max_page_size = 50000
    page_size = 50000
    paginate_by = 10000
    paginate_by_param ='page_size' # Allow client to override, using `?page_size=xxx`.

    filterset_fields = ['entry__mabid', 'sample_name', 'plate_location', 'volume', 'concentration', 'comments',
                        'failure', 'inline_index_name', 'inline_index', 'LCs_reported', 'HCs_reported']
    search_fields = ['entry__mabid', 'sample_name', 'plate_location', 'volume', 'concentration', 'comments',
                        'failure', 'inline_index_name', 'inline_index', 'LCs_reported', 'HCs_reported']
    ordering_fields = '__all__'


class StatusCSVExportView(View):
    serializer_class = TrimmerStatusSerializer

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(
            queryset,
            many=many,
        )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        serializer = self.get_serializer(
            TrimmerEntryStatus.objects.all(),
            many=True
        )
        header = TrimmerStatusSerializer.Meta.fields

        writer = csv.DictWriter(response, fieldnames=header)
        writer.writeheader()
        for row in serializer.data:
            writer.writerow(row)

        return response