from django.template import loader
from django.forms import ModelForm
from .models import *
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, CreateView, FormMixin

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
import subprocess
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

# API STUFF
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets
from .methods import *
from rest_framework import filters

from django.contrib.auth import login, authenticate, logout
import plotly.express as px
import urllib
import json
from .forms import *
from django.utils.decorators import method_decorator
from django.db.models import Count
from .methods import *
from django.db.models import Q

import xmltodict
import pandas as pd
import numpy as np
import plotly.io as pio
import collections
import pandas as pd


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# def summary_plate_view(request):
#     all = TrimmerSequence.objects.all().values('plate').annotate(total=Count('plate')).order_by('total')
#     for item in all:
#         print(item)
#
#     count_dict = {}
#     seqs = TrimmerSequence.objects.all()
#     for seq in seqs:
#         if seq.plate in count_dict.keys():
#             if seq.entry.mabid in count_dict[seq.plate].keys():# and seq.entry.show_on_web is True:
#                 count_dict[seq.plate][seq.entry.mabid]+=1
#             else: #if seq.entry.show_on_web is True:
#                 count_dict[seq.plate][seq.entry.mabid]=1
#         else:
#             count_dict[seq.plate] = {}
#     sum = 0
#     for key in count_dict.keys():
#         print(key + ' ' + str(len(count_dict[key].keys())))
#         sum +=  len(count_dict[key].keys())
#
#     print("TOTAL MABIDS: " + str(sum))
#


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



def signup(request):
    context = {}
    if request.method == 'POST':
        main_form = SignUpForm(request.POST)

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
        if result['success']:
            if main_form.is_valid():
                main_form.save()
                username = main_form.cleaned_data.get('username')
                raw_password = main_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("Main Page")
            else:
                context['errors'] = main_form.errors
                context['main_form'] = SignUpForm(request.POST)
        else:
            context['main_form'] = SignUpForm(request.POST)
    else:
        context['main_form'] = SignUpForm()

    return render(request, 'registration/signup.html', context)


def FAQListView(request):

    context= {}
    context['questions'] = FAQ.objects.filter(is_definition=False)
    context['definitions'] = FAQ.objects.filter(is_definition=True)

    return render(request, 'faq_list.html', context)


def MyLogout(request):
    logout(request)
    return redirect('/')


# TODO fix this so to filter pos and neg from Light and Heavy
def main_page(request):
    html = 'home.html'
    context = {}
    all_entries = TrimmerEntry.objects.filter(show_on_web=True)
    all_entries = all_entries.exclude(mabid__contains='positive')
    all_entries = all_entries.exclude(mabid__contains='negative')
    context['total_number_entries'] = len(all_entries)
    context['total_number_light'] = len(TrimmerSequence.objects.filter(chain="Light",
                                                                       anarci_bad=False,
                                                                       anarci_duplicate=False,
                                                                       bad_support=False,
                                                                       entry__show_on_web=True
                                                                       ))
    context['total_number_heavy'] = len(TrimmerSequence.objects.filter(chain="Heavy",
                                                                       anarci_bad=False,
                                                                       anarci_duplicate=False,
                                                                       bad_support=False,
                                                                       entry__show_on_web=True
                                                                       ))

    context['monoclonal_number_entries'] = len(all_entries.filter(~Q(category__in=[4,5])))
    context['monoclonal_number_light'] = len(TrimmerSequence.objects.filter(chain="Light",
                                                                            anarci_bad=False,
                                                                            bad_support=False,
                                                                            anarci_duplicate=False,
                                                                            entry__show_on_web=True).exclude(entry__category__in=[4,5]))
    context['monoclonal_number_heavy'] = len(TrimmerSequence.objects.filter(chain="Heavy",
                                                                            anarci_bad=False,
                                                                            bad_support=False,
                                                                            anarci_duplicate=False,
                                                                            entry__show_on_web=True).exclude(entry__category__in=[4,5]))

    context['parental_number_entries'] = len(all_entries.filter(category__in=[4,5]))
    context['parental_number_light'] = len(TrimmerSequence.objects.filter(chain="Light",
                                                                          entry__category__in=[4,5],
                                                                          anarci_bad=False,
                                                                          bad_support=False,
                                                                          anarci_duplicate=False))
    context['parental_number_heavy'] = len(TrimmerSequence.objects.filter(chain="Heavy",
                                                                          entry__category__in=[4,5],
                                                                          anarci_bad=False,
                                                                          anarci_duplicate=False,
                                                                          bad_support=False,
                                                                          ))

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



@staff_member_required
def add_faq(request):
    if request.method == 'POST':
        form = AddFAQ(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            question = form.cleaned_data['question']
            is_definition = form.cleaned_data['is_definition']

            new_faq = FAQ.objects.create(message=message,
                                         question=question,
                                         is_definition=is_definition
                                             )
            new_faq.save()
            return redirect('/faq_list/')
    else:
        form = AddFAQ()
    return render(request, 'add_faq.html', {'form': form})


# @method_decorator(staff_member_required, name='dispatch')
@staff_member_required
def edit_faq(request, pk):
    context = {}
    if request.method == 'POST':
        form = AddFAQ(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            question = form.cleaned_data['question']
            is_definition = form.cleaned_data['is_definition']

            update_faq = FAQ.objects.get(pk=pk)
            update_faq.message = message
            update_faq.question = question
            update_faq.is_definition = is_definition
            update_faq.save()

            return redirect('/faq_list/')
    else:
        context['faq'] = FAQ.objects.get(pk=pk)
        context['form'] = AddFAQ(initial={'message': context['faq'].message, 'question': context['faq'].question,
                                          'is_definition': context['faq'].is_definition})
    return render(request, 'faq_form.html', context)


@staff_member_required
def delete_faq(request, pk):
    faq = FAQ.objects.get(pk=pk)
    faq.delete()
        # context['form'] = AddFAQ(initial={'message': faq.message, 'question': faq.question, 'is_definition': faq.is_definition})
    return redirect('/faq_list/')



#
# def GetAsvGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[float(i) for i in df_l['asv_support'] if i is not None], [float(i) for i in df_h['asv_support'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = px.box()
#     figure.add_trace(go.Box(y=values[0], quartilemethod="inclusive", name="Light Chain ASV Count"))
#     figure.add_trace(go.Box(y=values[1], quartilemethod="inclusive", name="Heavy Chain ASV Count"))
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div


# def GetPctGraph():
#     """
#         Making the Pie Chart Summary for the General Views (either for an invoice or a dairy)
#     """
#     df_l = pd.DataFrame(list(TrimmerLight.objects.filter().values()))
#     df_h = pd.DataFrame(list(TrimmerHeavy.objects.filter().values()))
#     values = [[float(i) for i in df_l['pct_support'] if i is not None], [float(i) for i in df_h['pct_support'] if i is not None]]
#     group_labels = ['Light Chain', 'Heavy Chain']  # name of the dataset
#
#     figure = px.box()
#     figure.add_trace(go.Box(y=values[0], quartilemethod="inclusive", name="Light Chain Percent Support"))
#     figure.add_trace(go.Box(y=values[1], quartilemethod="inclusive", name="Heavy Chain Percent Support"))
#     div = opy.plot(figure, auto_open=False, output_type='div')
#
#     return div



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

def blat(request,query_seq):
    context = {}
    context['queryset'] = None
    if request.method == 'POST':
        form = Blat(request.POST)
        if form.is_valid():
            # Get the From Data

            ''' Begin reCAPTCHA validation '''
            # recaptcha_response = request.POST.get('g-recaptcha-response')
            # url = 'https://www.google.com/recaptcha/api/siteverify'
            # values = {
            #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #     'response': recaptcha_response
            # }
            # data = urllib.parse.urlencode(values).encode()
            # req = urllib.request.Request(url, data=data)
            # response = urllib.request.urlopen(req)
            # result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            sequence = form.cleaned_data['sequence']
            #category_types = form.cleaned_data["category"]
            type = form.cleaned_data['type']
            search_prefix = form.cleaned_data['search_prefix'].replace('/','_')
            context['form'] = Blat(initial={"sequence": sequence, "type":type, "search_prefix":search_prefix.replace('_','/')})

            # if not result['success']:
            #     return render(request, 'blat.html', context)

            # getwd so it works on cluster too because i think subprocess needs absolute
            cwd = os.getcwd()
            prefix = '/'.join(cwd.split('/')[:-1])

            # Create  some temp files (query file .fa and psl) for running BLAT
            rand_string = get_random_string(10)
            file_name = '%s/static_data/%s.fa' % (prefix, rand_string)
            with open(file_name, 'w') as temp_file:
                temp_file.write('>%s' % rand_string + '\n')
                temp_file.write(sequence)
            psl = '%s/static_data/%s.psl' % (prefix, rand_string)


            # If prefix create a new files that will be used instead of the file with all entries
            if search_prefix:
                search_prefix_file_name = '%s/static_data/%s.fa' % (prefix, search_prefix)
                with open(search_prefix_file_name, 'w') as temp_file:
                    if form.cleaned_data["clonality"]:
                        sequences = TrimmerSequence.objects.filter(entry__mabid__contains=search_prefix.replace('_','/'),
                                                                   clonality=form.cleaned_data["clonality"],
                                                                   anarci_bad=False,
                                                                   bad_support=False,
                                                                   anarci_duplicate=False)
                    else:
                        sequences = TrimmerSequence.objects.filter(entry__mabid__contains=search_prefix.replace('_', '/'),
                                                                   anarci_bad=False,
                                                                   bad_support=False,
                                                                   anarci_duplicate=False)
                    for seq in sequences:
                        testing = get_header(seq, seq.chain)
                        temp_file.write(get_header(seq, seq.chain))
                        if type=="dna":
                            temp_file.write(seq.seq + '\n')
                        else:
                            temp_file.write(seq.aa + '\n')
                call = "blat %s %s -t=%s -q=%s %s" % (search_prefix_file_name, file_name, type, type, psl)
            else:
                call = "blat %s/static_data/%s.fa %s -t=%s -q=%s %s" % (prefix, type, file_name, type, type, psl)
            # print(call)
                # os.popen(call).read()

            # print (call.split(' '))
            #"source activate ~/.bash_profile;" +
            if 'ubuntu' in prefix:
                process = subprocess.Popen(['/bin/bash', '-c', "source ~/.bashrc; export PATH='/home/ubuntu/anaconda3/bin:$PATH'; eval echo ~$USER; source activate trimmer_lab;".replace("\n",' ') + call], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                process = subprocess.Popen(['/bin/bash', '-c', call], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, err = process.communicate()
            #context['err'] = err
            #context['out'] = out
            #context['prefix'] = prefix
            # print(err)
            # print(out)
            process.wait()

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
                    temp_dict['pk'] = parse_id[0]
                    temp_dict['mabid'] = parse_id[1]
                    temp_dict['entry_pk'] = parse_id[2]
                    temp_dict['chain'] = parse_id[5]
                    #temp_dict['plate'] = parse_id[4]
                    temp_dict['chain_id'] = parse_id[7]
                    temp_dict['clonality'] = parse_id[8]
                    if temp_dict["clonality"] and temp_dict["clonality"] == form.cleaned_data["clonality"]:
                        all_results.append(temp_dict)
                #print(parse_id)


            context['queryset'] = list(sorted(all_results, key=lambda d: (d['score'], d['ident_pct']), reverse=True))

            # Temp file cleanup for search prefix temp file and rand string file from query
            if search_prefix:
                call_sprm = 'rm %s %s' % (search_prefix_file_name, psl)

                process = subprocess.Popen(call_sprm.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                process.wait()

            call = 'rm %s %s' % (file_name, psl)
            process = subprocess.Popen(call.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            process.wait()

            return render(request, 'blat.html', context)
        else:
            context['errors'] = form.errors
            context['form'] = Blat()
            return render(request, 'blat.html', context)

    else:
        if query_seq == "None":
            context['form'] = Blat()
        else:
            context['form'] = Blat(initial={"sequence": query_seq})

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


# class EntryDetailView(DetailView):
#     model = Entry
#     template_name = 'entry.html'
#
#     def get_object(self, *args, **kwargs):
#         obj = super(EntryDetailView, self).get_object(*args, **kwargs)
#         return obj
#
#     def get_context_data(self, **kwargs):
#         # make sure that the invoices are not too many for the view but are still graphed
#         context = super().get_context_data(**kwargs)
#         context['entry'] = Entry.objects.get(pk=self.kwargs['pk'])
#         return context


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
        try:
            context['pk2'] = self.kwargs['pk2']
        except:
            context['pk2'] = 0
        context['light'] = TrimmerSequence.objects.filter(entry=context['entry'],
                                                          duplicate=False,
                                                          chain="Light",
                                                          anarci_duplicate=False,
                                                          bad_support=False,
                                                          anarci_bad=False).exclude(aa='-').order_by('asv_order')
        # context['light_duplicates'] = TrimmerLight.objects.filter(entry=context['entry'], duplicate=True)
        context['heavy'] = TrimmerSequence.objects.filter(entry=context['entry'],
                                                          duplicate=False,
                                                          chain="Heavy",
                                                          anarci_duplicate=False,
                                                          bad_support=False,
                                                          anarci_bad=False).exclude(aa='-').order_by('asv_order')
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




#@staff_member_required
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


def query_dict_to_string(querydict):
    string = '?'
    string_list = []
    for i in querydict.keys():
        string_list.append(i + '=' + querydict[i])
    return string + '&'.join(string_list)

def SequenceListView(request):
    context = {}
    all_entries = TrimmerSequence.objects.filter(entry__show_on_web=True).exclude(aa='-')
    context['filter'] = TrimmerSequenceFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs[:200]
    context['querystring'] = query_dict_to_string(request.GET)
    return render(request, 'query.html', context)


def fasta_file_response(request):
    context = {}
    all_entries = TrimmerSequence.objects.filter(entry__show_on_web=True,
                                                 anarci_bad=False,
                                                 bad_support=False,
                                                 anarci_duplicate=False).exclude(aa='-')
    context['filter'] = TrimmerSequenceFilter(request.GET, queryset=all_entries)
    context['queryset'] = context['filter'].qs[:200]
    filename = "neuromabseq_export.fa"
    content = ''
    # TODO Need to fix this based on the updated Heavy and Light chain pks
    for i in context["queryset"]:
        content += get_header(i, i.chain, i.asv_order)
        content += i.seq + '\n'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


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
    filterset_fields = ["category", "mabid", "protein_target", "clonality"]
    # property_fields = [
    #     ('clonality', DjangoFilterBackend, ['exact']),
    # ]
    # filterset_fields = {
    #     'category': ["in","exact"], # icontains ,exact, gte, lte, in
    #     'mabid': ["exact",],
    #     'protein_target': ["exact",],
    # }
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

    filterset_fields = ['entry__mabid', 'entry__category', 'sample_name', 'plate_location', 'volume', 'concentration', 'comments',
                        'failure', 'inline_index_name', 'inline_index', 'LCs_reported', 'HCs_reported']
    search_fields = ['entry__mabid',  'entry__category','sample_name', 'plate_location', 'volume', 'concentration', 'comments',
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



"""
LISA STUFF
"""

def xml_to_dict(
    filename: str
)-> dict:
    # Open the file and read the contents
    with open(filename, 'rb') as file:
        my_xml = file.read()
        file.close()

    my_dict = xmltodict.parse(my_xml)
    return my_dict


def deep_convert_dict(
    layer: dict
) -> dict:
    to_ret = layer
    if isinstance(layer, collections.OrderedDict):
        to_ret = dict(layer)

    try:
        for key, value in to_ret.items():
            to_ret[key] = deep_convert_dict(value)
    except AttributeError:
        pass

    return to_ret


def lisa_process(
        context: dict,
        flisa_path: str,
        elisa_path: str,
        pos_control1: str,
        pos_control2: str,
        neg_control1: str,
        neg_control2: str,
) -> dict:
    """
    :param context:
    :param flisa_path:
    :param elisa_path:
    :param pos_control1:
    :param pos_control2:
    :param neg_control1:
    :param neg_control2:
    :return:
    """

    # ELISA
    master_list = []
    for i in range(0, len(xml_to_dict(filename=elisa_path)["Experiment"]["PlateSections"])):
        get_just_reduced = deep_convert_dict(xml_to_dict(filename=elisa_path)["Experiment"]["PlateSections"][i])
        get_just_reduced = get_just_reduced["PlateSection"]["reducedData"]["Well"]
        for w in get_just_reduced:
            w = deep_convert_dict(w)
            w["plate"] = i + 1
            master_list.append(w)
    df_e = pd.DataFrame.from_records(master_list)

    # FLISA
    master_list = []
    start_dict = xml_to_dict(filename=flisa_path)["Experiment"]["PlateSections"]
    for i in range(0, len(start_dict)):
        get_just_reduced = deep_convert_dict(start_dict[i])
        get_just_reduced = get_just_reduced["PlateSection"]
        get_just_reduced = deep_convert_dict(get_just_reduced["Wavelengths"]["Wavelength"])
        for wv in range(0, len(get_just_reduced)):
            grab_wavelength = deep_convert_dict(get_just_reduced[wv])["@WavelengthIndex"]
            get_just_reduced_wv = deep_convert_dict(get_just_reduced[wv])
            get_just_reduced_wells = [deep_convert_dict(i) for i in get_just_reduced_wv["Wells"]["Well"]]
            for w in get_just_reduced_wells:
                w["wavelength"] = grab_wavelength
                w["plate"] = i + 1
                master_list.append(w)

    df_f = pd.DataFrame.from_records(master_list)
    df_f.index = df_f["@Name"] + "_Plate" + df_f["plate"].astype(str)
    df_f = df_f[["RawData", "wavelength"]].pivot(columns='wavelength').droplevel(0, axis=1)


    # Normalize to well after merging ELISA and FLISA
    df_e.index = df_e["@Name"] + "_Plate" + df_e["plate"].astype(str)
    # add the plate to help with normalization process
    final_df = df_e.merge(df_f, left_index=True, right_index=True)

    master_norm_list = []
    for i in set(final_df["plate"].to_list()):
        # filter for the plate
        temp_fil = final_df[final_df["plate"] == i][["reducedVal", "1", "2", "3"]]

        # fix the column types
        for col in temp_fil.columns:
            temp_fil[col] = temp_fil[col].astype(float)
            # lets log scale this as well
            temp_fil[col] = np.log2(temp_fil[col])

        # get the positive control and divide by it
        pos_control1 = temp_fil.loc["A1_Plate" + str(i)]
        pos_control2 = temp_fil.loc["A12_Plate" + str(i)]
        pos_control = (pos_control1 + pos_control2) / 2
        temp_fil = temp_fil / pos_control

        # column sum normalize
        for col in temp_fil.columns:
            temp_fil[col] = temp_fil[col] / temp_fil[col].sum()

        # pos_control = temp_fil.loc[["A1_Plate" + str(i), "A12_Plate" + str(i)]]

        master_norm_list.append(temp_fil)

    final_df = pd.concat(master_norm_list)
    final_df.columns = ["ELISA", "FLISAwv1", "FLISAwv2", "FLISAwv3"]
    final_df["Control"] = ""
    for index, row in final_df.iterrows():
        if "A12_" in index or "A1_" in index:
            final_df.at[index, "Control"] = "Positive Control"
        if "H1_" in index or "H12_" in index:
            final_df.at[index, "Control"] = "Negative Control"
    final_df["Name"] = final_df.index
    final_df["F1_E"] = final_df["FLISAwv1"] + final_df["ELISA"]
    final_df["F2_E"] = final_df["FLISAwv2"] + final_df["ELISA"]
    final_df["F3_E"] = final_df["FLISAwv3"] + final_df["ELISA"]
    final_df["FLISA"] = final_df["FLISAwv1"] + final_df["FLISAwv2"] + final_df["FLISAwv3"]
    final_df["Max"] = final_df[["FLISAwv1", "FLISAwv2", "FLISAwv3"]].idxmax(axis=1)

    fig = px.scatter(final_df, x="ELISA", y="FLISAwv1", color="Control", symbol="Max",
                     hover_data=["Name", "FLISAwv2", "FLISAwv3"])
    context['graph_wv1'] = fig.to_html()
    fig = px.scatter(final_df, x="ELISA", y="FLISAwv2", color="Control", symbol="Max",
                     hover_data=["Name", "FLISAwv1", "FLISAwv3"])
    context['graph_wv2'] = fig.to_html()
    fig = px.scatter(final_df, x="ELISA", y="FLISAwv3", color="Control", symbol="Max",
                     hover_data=["Name", "FLISAwv1", "FLISAwv2"])
    context['graph_wv3'] = fig.to_html()
    fig = px.scatter(final_df, x="ELISA", y="FLISA", color="Control", symbol="Max",
                     hover_data=["Name", "FLISAwv1", "FLISAwv2", "FLISAwv3"])
    context['graph_all'] = fig.to_html()

    final_df["ELISA_pow"] = final_df["ELISA"] + 10
    fig = px.scatter_3d(final_df, x="FLISAwv1", y="FLISAwv2", z="FLISAwv3",
                        color="Control", size="ELISA_pow")
    context['graph_3d'] = fig.to_html()

    return context

def lisa(request):
    context = {}
    if request.method == 'POST':
        main_form = LISAForm(request.POST, request.FILES)

        if main_form.is_valid():
            elisa = main_form.cleaned_data['elisa_reduced_xml'].file.name
            flisa = main_form.cleaned_data['flisa_raw_xml'].file.name
            context = lisa_process(context=context,
                                   elisa_path=elisa,
                                   flisa_path=flisa,
                                   pos_control1="A1",
                                   pos_control2="A2",
                                   neg_control1="H1",
                                   neg_control2="H12")
            context['main_form'] = LISAForm()
            return render(request, 'lisa.html', context)
        else:
            context['errors'] = main_form.errors
            context['main_form'] = LISAForm(request.POST)

    else:
        context['main_form'] = LISAForm()

    return render(request, 'lisa.html', context)
