
from django import forms
from django.views.generic.edit import FormView, ModelFormMixin
from .models import *
from django import forms
from django.forms import ModelForm, Textarea
from django.db.models.fields import PositiveIntegerField


class Blat(forms.Form):
    sequence = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={"rows": 10, "cols": 100}))
    type = forms.ChoiceField(required=True, choices=(("dna", "DNA"), ("protein","Protein")), initial='DNA')

