from django import forms
from .models import Place, TravelTime


class TicketForm(forms.Form):
    name = forms.CharField(label='name', max_length=20)
    telephone = forms.IntegerField(label='telephone')
    seat = forms.IntegerField(label='seat')
    code = forms.CharField(max_length=10)

