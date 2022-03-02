from django import forms
from .models import Email


class ComposeForm(forms.ModelForm):
    """Form for the new email model"""

    class Meta:
        model = Email
        fields = ['receiver', 'cc', 'bcc', 'subject', 'body', 'file']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('body', 'file')
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class SearchForm(forms.Form):
    search = forms.CharField()
