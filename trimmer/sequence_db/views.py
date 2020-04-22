from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from django.views.generic import DetailView
from .filters import *
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
from .methods import *


def main_page(request):
    html = 'home.html'
    context = {}
    context['number_entries'] = len(TrimmerEntry.objects.filter())
    context['number_light'] = len(TrimmerLight.objects.filter(duplicate=False))
    context['number_heavy'] = len(TrimmerHeavy.objects.filter(duplicate=False))
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

    figure = ff.create_distplot(values, group_labels, bin_size=200)
    figure.update_layout(title_text='Distribution of ASV Counts for Heavy Chain vs Light Chain')
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

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Percent Support for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetScoreGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[float(i) for i in df_l['score'] if i is not None], [float(i) for i in df_h['score'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Score for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetSeqGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[len(i) for i in df_l['seq'] if i is not None], [len(i) for i in df_h['seq'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Sequence Length for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetAAGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[len(i) for i in df_l['aa'] if i is not None], [len(i) for i in df_h['aa'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Amino Acid Length for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetDomainGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[len(i) for i in df_l['aa'] if i is not None], [len(i) for i in df_h['domain'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Coding Domain Length for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetSeqStopGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))

    df_l = df_l.replace([np.inf, -np.inf], np.nan).dropna(how="all")
    df_h = df_h.replace([np.inf, -np.inf], np.nan).dropna(how="all")

    values = [[i for i in df_l['seq_stop_index'] if i is not None], [i for i in df_h['seq_start_index'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Sequence Stop Index for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def GetSeqStartGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))

    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))

    df_l = df_l.replace([np.inf, -np.inf], np.nan).dropna(how="all")
    df_h = df_h.replace([np.inf, -np.inf], np.nan).dropna(how="all")

    values = [[i for i in df_l['seq_start_index'] if i is not None], [i for i in df_h['seq_start_index'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Sequence Start Index for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def ScoreGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[len(i) for i in df_l['score_index'] if i is not None], [len(i) for i in df_h['score_index'] if i is not None]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Sequence Length for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div


def analytics_view(request):
    context = {}
    context['graph'] = GetAsvGraph()
    context['graph_pct'] = GetPctGraph()
    context['graph_seq'] = GetSeqGraph()
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
        context['light'] = TrimmerLight.objects.filter(entry=context['entry'], duplicate=False)
        # context['light_duplicates'] = TrimmerLight.objects.filter(entry=context['entry'], duplicate=True)
        context['heavy'] = TrimmerHeavy.objects.filter(entry=context['entry'], duplicate=False)
        # context['heavy_duplicates'] = TrimmerHeavy.objects.filter(entry=context['entry'], duplicate=True)
        #context['graph'] = GetAsvGraph()
        #context['graph_pct'] = GetPctGraph()
        #context['graph_seq'] = GetSeqGraph()

        #context['graph_h'] = GetHeavyAsvGraph()
        return context


def TrimmerEntryListView(request):
    context = {}
    all_entries = TrimmerEntry.objects.all()
    context['filter'] = TrimmerEntryFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs.order_by('mabid')
    return render(request, 'new_query.html', context)


def TrimmerStatusListView(request):
    context = {}
    context['all_entries'] = TrimmerEntryStatus.objects.all()
    context['status_entries'] = [i.entry.mabid for i in TrimmerEntryStatus.objects.all()]
    context['entries'] = [i.mabid for i in TrimmerEntry.objects.all()]
    context['status_not_in_entries'] = status_not_present()
    context['entries_not_in_status'] = sorted(list(set(context['entries']) - set(context['status_entries'])))
    # TODO plate stats for this view
    context['plate_stats'] = ''
    return render(request, 'status_list.html', context)


def EntryListView(request):
    context = {}
    all_entries = Entry.objects.all()
    context['filter'] = EntryFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs.order_by('-name')
    return render(request, 'query.html', context)


