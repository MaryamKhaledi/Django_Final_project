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
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام کاربری', 'class': 'form-control'}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'کلمه عبور', 'class': 'form-control'}),
        label='کلمه عبور'
    )

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        is_exists_user = User.objects.filter(username=user_name).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات یافت شده ثبت نام نکرده است')
        return user_name
