from django import forms
from django.core.exceptions import ValidationError
from django.forms import EmailInput
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets, ModelForm
from accounts.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'recovery', 'email', 'phone_number', 'birth_date',
            'gender', 'country')
        widgets = {'birth_date': widgets.DateInput(attrs={'type': 'date'})}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class VerifyCodeForm(forms.ModelForm):
    class Meta:
        model = OtpCode
        fields = ('code',)

# ..........Z....................

# class DateInput(forms.DateInput):
#     input_type = 'date'
#
#
# class UserRegisterForm(forms.Form):
#     class Meta:
#         model = User
#         fields = ['username',
#                   'first_name',
#                   'last_name',
#                   'birth_date',
#                   'email',
#                   'phone_number',
#                   'password1',
#                   'password2'
#                   'gender',
#                   'country',
#                   ]
#         widgets = {
#             'birthdate': DateInput(),
#         }
#
#
# class VerifyCodeForm(forms.Form):
#     code = forms.IntegerField()

# class UserLoginForm(forms.Form):
#     username = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'khaledi.maryam74@eml.com.com'}))
#     password = forms.CharField(label='password',
#                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}))


# class ResetPasswordForm(forms.Form):
#     recovery_email = forms.EmailField(
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'khaledi.maryam74@eml.com.com'}),
#         required=False)
#     phone_number = forms.CharField(label='phone_number',
#                                    widget=forms.TextInput(
#                                        attrs={'class': 'form-control', 'placeholder': '0916********'}),
#                                    required=False)
#
#
# class ResetPasswordConfirmForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['password1', 'password2']
#
#     password1 = forms.CharField(label='password',
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                                   'placeholder': '******'}))
#     password2 = forms.CharField(label='password',
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control',
#                                                                   'placeholder': '******'}))
#
#
