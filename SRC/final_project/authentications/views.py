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


def index(request):
    return render(request, "authentications/index.html")


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
            if user.is_active:
                login(request, user)
                return redirect('mail_page:inbox')
            else:
                return render(request, 'authentications/login.html',
                              messages.error(request, f"{request.POST.get('username')} is not active"))
        else:
            return render(request, 'authentications/login.html',
                          messages.error(request, 'You password or Email is incorrect'))


# class LoginView(View):
#     form_class = LoginForm
#     template_name = 'authentications/login.html'
#
#     def setup(self, request, *args, **kwargs):
#         self.next = request.GET.get('next')
#         return super().setup(request, *args, **kwargs)
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('mail_page:home')
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         form = self.form_class
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'you logged in successfully', 'success')
#                 if self.next:
#                     return redirect(self.next)
#                 return redirect('mail_page:compose')
#             messages.error(request, 'username or password is wrong', 'warning')
#         return render(request, self.template_name, {'form': form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'authentications/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
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
            print('ghabl as if')
        if user is not None and account_activation_token.check_token(user, token):
            print('ghabl as active')
            user.is_active = True
            user.username += '@eml.com'
            # user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))

            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


# class LogoutView(LoginRequiredMixin, View):
#     def get(self, request):
#         logout(request)
#         messages.success(request, 'you logged out successfully', 'success')
#         return redirect('login')

def logout(request):
    # logout(request)
    return redirect('login')
