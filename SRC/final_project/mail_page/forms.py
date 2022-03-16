from django import forms
from django.forms import RadioSelect

from .models import Email, Contacts, Label, Signature, Filter


class ComposeForm(forms.ModelForm):
    """Form for the new email model"""

    class Meta:
        model = Email
        fields = ['receiver', 'cc', 'bcc', 'subject', 'body', 'file', 'status']


class NewSignatureForm(forms.ModelForm):
    """Form for the new label model"""

    class Meta:
        model = Signature
        fields = ['title']


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('subject', 'body', 'file')
        # todo : add signature
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class ForwardForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('receiver', 'cc', 'bcc')
        # todo : add signature
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class NewContactForm(forms.ModelForm):
    """Form for the new contact model"""

    class Meta:
        model = Contacts
        fields = ['name', 'email', 'phone_number', 'other_email', 'birth_date']

        widgets = {
            'birthdate': DateInput(),
        }


class NewLabelForm(forms.ModelForm):
    """Form for the new label model"""

    class Meta:
        model = Label
        fields = ['title']


class SearchForm(forms.Form):
    search = forms.CharField()


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['sender', 'subject', 'body','file' ,'action']
        # file = forms.TypedChoiceField(widget=forms.RadioSelect)
        file = forms.BooleanField(widget=RadioSelect(choices=[(True, 'Yes'),
                                                              (False, 'No')]))
