from django import forms
from .models import Ticket, Comment, Fund

class TicketSubmitForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'type',
            'title',
            'content',
            'author',
            'last_modified',
        )
        widgets = {
            'author': forms.HiddenInput(),
            'last_modified': forms.HiddenInput(),
        }

class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'title',
            'content',
            'last_modified',
        )
        widgets = {
            'author': forms.HiddenInput(),
            'last_modified': forms.HiddenInput(),
        }

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
            'author',
            'ticket',
        )
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'author': forms.HiddenInput(),
            'ticket': forms.HiddenInput(),
        }
        labels = {
            'content': 'New Comment',
        }

class FundingForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = (
            'fund',
            'user',
            'ticket',
        )
        widgets = {
            'user': forms.HiddenInput(),
            'ticket': forms.HiddenInput(),
        }
        labels = {
            'fund': 'How much would you like to put towards this feature request? (in GBP £/ Minimum: £1.00)',
        }

class CardDetailForm(forms.Form):
    MOHTH_CHOICES = [ (i, i) for i in range(1,13)]
    YEAR_CHOICES = [ (i, i) for i in range(2018, 2037)]

    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MOHTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'status',
        )

class UpdateThresholdForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            'threshold',
        )
