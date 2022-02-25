from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .forms import *
from .tokens import account_activation_token


# def register(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#
#         form = RegisterForm()
#
#         if request.method == "POST":
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, 'Account was created for' + user)
#                 return redirect('login')
#         context = {'form': form}
#         return render(request, 'authentications/register.html', context)

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.info(request, 'Username or password is incorrect')
#         context = {}
#         return render(request, 'authentications/login.html', context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authentications/login.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            user_login = User.objects.get(username=username)
            # برای گرفتن ایدی کاربر که لاگین شده با ایمیل
            if user.is_active:
                login(request, user)
                return redirect('inbox', pk=user_login.id)
            else:
                return render(request, '')


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = self.RegisterForm()
        return render(request, 'authentications/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('authentications/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return redirect('login')
        else:
            messages.error(request, 'register failed')
            return redirect('logout')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.username += '@eml.com'
            # user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('register')


def logout(request):
    logout(request)
    return redirect('login')
