from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.forms import ModelForm
from .models import *
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, FormMixin

from .filters import *
import pandas as pd
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.figure_factory as ff
import numpy as np
from .methods import *
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required


# API STUFF
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from django.contrib.auth import login, authenticate, logout
import plotly.express as px
import urllib
import json
from .forms import *
from django.utils.decorators import method_decorator


class MyLoginView(auth_views.LoginView):
    # ratelimit_key = 'ip'
    # ratelimit_rate = '10/h'
    # ratelimit_block = True

    def form_valid(self, form):
        request_body = self.request.POST
        if not request_body:
            return None

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
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

        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if result['success'] and user is not None:
            return super().form_valid(form)
        else:
            return redirect('login')

@method_decorator(staff_member_required, name='dispatch')
class FAQListView(ListView):
    model = FAQ
    template_name = 'faq_list.html'


def MyLogout(request):
    logout(request)
    html = 'home.html'
    context = None
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))



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


@staff_member_required
def edit_metadata(request):
    context = {}
    if request.method == 'POST':
        if 'general_file_form' in request.POST:
            form = GeneralFileForm(request.POST, request.FILES)
            if form.is_valid():
                file_path = form.cleaned_data['general_file'].file.name
                metadata_file_process(context, file_path)
            else:
                context['errors'] = form.errors

    context['form'] = GeneralFileForm()
    return render(request, 'edit_metadata.html', context)


class FAQListView(ListView):
    model = FAQ
    template_name = 'faq_list.html'


@staff_member_required
def add_faq(request):
    if request.method == 'POST':
        form = AddFAQ(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            question = form.cleaned_data['question']

            new_faq = FAQ.objects.create(message=message,
                                         question=question,
                                             )
            new_faq.save()
            return redirect('/faq_list/')
    else:
        form = AddFAQ()
    return render(request, 'add_faq.html', {'form': form})


# @method_decorator(staff_member_required, name='dispatch')
@staff_member_required
def edit_faq(request, pk):
    if request.method == 'POST':
        form = AddFAQ(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            question = form.cleaned_data['question']

            update_faq = FAQ.objects.get(pk=pk)
            update_faq.message = message
            update_faq.question = question
            update_faq.save()

            return redirect('/faq_list/')
    else:
        faq = FAQ.objects.get(pk=pk)
        form = AddFAQ(initial={'message': faq.message, 'question': faq.question})
    return render(request, 'add_faq.html', {'form': form})


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
    context['all_entries'] = TrimmerEntryStatus.objects.all()

    context['status_entries'] = [i.entry.mabid for i in TrimmerEntryStatus.objects.all()]
    context['entries'] = [i.mabid for i in TrimmerEntry.objects.all()]
    context['entries'] = [i.mabid for i in TrimmerEntry.objects.all()]
    context['status_not_in_entries'] = status_not_present()
    context['entries_not_in_status'] = sorted(list(set(context['entries']) - set(context['status_entries'])))
    context['messages'] = Messages.objects.all()
    context['messages'] = [i.message.split(':')[1].replace(' ', '') for i in context['messages'] if 'metadata' in i.message]
    context['metadata_minus_status'] = sorted(list(set(context['messages']) - set(context['status_entries'])))
    context['status_minus_metadata'] = sorted(list(set(context['status_entries']) - set(context['messages'])))

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


