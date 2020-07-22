from .models import *
from django import forms


class GeneralFileForm(forms.Form):
    general_file = forms.FileField(required=True)


class AddFAQ(forms.Form):
    question = forms.CharField(max_length=4000, required=True, widget=forms.Textarea(attrs={"rows":5, "cols":100}))
    message = forms.CharField(max_length=4000, required=True, widget=forms.Textarea(attrs={"rows":5, "cols":100}))

    class Meta:
        model = FAQ
        fields = ('question','message',)
