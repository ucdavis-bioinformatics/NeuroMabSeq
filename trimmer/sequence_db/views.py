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


def main_page(request):
    html = 'home.html'
    context = {}
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))

def GetAsvGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[i for i in df_l['asvcount']], [i for i in df_h['asvcount']]]
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
    values = [[float(i) for i in df_l['pctsupport']], [float(i) for i in df_h['pctsupport']]]
    group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset

    figure = ff.create_distplot(values, group_labels, bin_size=1)
    figure.update_layout(title_text='Distribution of Percent Support for Heavy Chain vs Light Chain')
    div = opy.plot(figure, auto_open=False, output_type='div')

    return div

def GetSeqGraph():
    """
        Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
    """
    df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
    df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
    values = [[len(i) for i in df_l['seq']], [len(i) for i in df_h['seq']]]
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
    model = Entry
    template_name = 'new_entry.html'

    def get_object(self, *args, **kwargs):
        obj = super(TrimmerEntryDetailView, self).get_object(*args, **kwargs)
        return obj

    def get_context_data(self, **kwargs):
        # make sure that the invoices are not too many for the view but are still graphed
        context = super().get_context_data(**kwargs)
        context['entry'] = TrimmerEntry.objects.get(pk=self.kwargs['pk'])
        context['light'] = TrimmerLight.objects.filter(entry=context['entry'])
        context['heavy'] = TrimmerHeavy.objects.filter(entry=context['entry'])
        context['graph'] = GetAsvGraph()
        context['graph_pct'] = GetPctGraph()
        context['graph_seq'] = GetSeqGraph()

        #context['graph_h'] = GetHeavyAsvGraph()
        return context



def TrimmerEntryListView(request):
    context = {}
    all_entries = TrimmerEntry.objects.all()
    context['filter'] = TrimmerEntryFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs.order_by('trimmerid')[:400]
    # print(context)
    return render(request, 'new_query.html', context)


def EntryListView(request):
    context = {}
    all_entries = Entry.objects.all()
    context['filter'] = EntryFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs.order_by('-name')[:400]
    # print(context)
    return render(request, 'query.html', context)


