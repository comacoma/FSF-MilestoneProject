from django import forms
from .models import *

class TicketPostForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'type',
            'title',
            'content',
        )
