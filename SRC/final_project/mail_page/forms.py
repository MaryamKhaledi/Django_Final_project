from django import forms
from .models import Email


class ComposeForm(forms.ModelForm):
    """Form for the new email model"""

    class Meta:
        model = Email
        fields = ['receiver', 'cc', 'bcc', 'subject', 'body', 'file']


class ReplyEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['receiver']
