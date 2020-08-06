
from django import forms
from django.views.generic.edit import FormView, ModelFormMixin
from .models import *
from django import forms
from django.forms import ModelForm, Textarea
from django.db.models.fields import PositiveIntegerField
from .models import *
from django import forms


class Blat(forms.Form):
    sequence = forms.CharField(max_length=1000, required=True, widget=forms.Textarea(attrs={"rows": 10, "cols": 100}))
    type = forms.ChoiceField(required=True, choices=(("dna", "DNA"), ("protein","Protein")), initial='DNA')


class GeneralFileForm(forms.Form):
    general_file = forms.FileField(required=True)


class AddFAQ(forms.Form):
    question = forms.CharField(max_length=4000, required=True, widget=forms.Textarea(attrs={"rows":5, "cols":100}))
    message = forms.CharField(max_length=4000, required=True, widget=forms.Textarea(attrs={"rows":5, "cols":100}))
    is_definition = forms.BooleanField(required=False, initial=False)

    # message = forms.

    class Meta:
        model = FAQ
        fields = ('question','message','is_definition')
