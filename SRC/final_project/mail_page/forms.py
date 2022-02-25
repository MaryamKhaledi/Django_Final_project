from django import forms
from .models import Email


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['receiver', 'subject', 'cc', 'bcc', 'body', 'file', 'signature', 'timestamp']


class ReplyEmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['receiver']
