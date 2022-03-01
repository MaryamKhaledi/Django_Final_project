from django import forms
from .models import Email


class NewEmailForm(forms.ModelForm):
    """Form for the email model"""

    class Meta:
        model = Email
        fields = ['receiver', 'subject', 'cc', 'bcc', 'body', 'file']


class ReplyEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['receiver']
