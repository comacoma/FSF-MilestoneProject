from django import forms
from .models import Ticket, Comment

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
