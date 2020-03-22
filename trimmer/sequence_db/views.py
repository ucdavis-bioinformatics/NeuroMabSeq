from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import *
from django.views.generic import DetailView
from .filters import *


def main_page(request):
    html = 'home.html'
    context = {}
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))


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


