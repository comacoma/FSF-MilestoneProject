from django import forms
from .models import *

class TicketSubmitForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'type',
            'title',
            'content',
            'author',
        )
        widgets = {
            'author': forms.HiddenInput()
        }
