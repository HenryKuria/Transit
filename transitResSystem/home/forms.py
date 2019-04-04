from django import forms
from .models import Place, TravelTime


class TicketForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    telephone = forms.IntegerField(label='telephone')
    seat = forms.IntegerField(label='seat')
    code = forms.CharField(max_length=10)


class FindForm(forms.Form):
    time = forms.ModelChoiceField(queryset=TravelTime.objects.all(), empty_label="---", required=True)
    start = forms.ModelChoiceField(queryset=Place.objects.all(), empty_label="---", required=True)
    end = forms.ModelChoiceField(queryset=Place.objects.all(), empty_label="---", required=True)
