import random
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from utils import send_otp_code
from .forms import *
from .tokens import account_activation_token
from accounts.models import OtpCode


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

            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')


def logout(request):
    # logout(request)
    return redirect('login')
# .........Z......................................
# class RegisterView(View):
#     def get(self, request, *args, **kwargs):
#         form = UserRegisterForm()
#         return render(request, 'authentications/register.html', {'forms': form})
#
#     def post(self, request, *args, **kwargs):
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             print(' vorod be form is valid')
#             if form.cleaned_data['email']:
#                 user = form.save(commit=False)
#                 user.is_active = False  # Deactivate account till it is confirmed
#                 user.save()
#                 current_site = get_current_site(request)
#                 subject = 'Activate Your MySite Account'
#                 message = render_to_string('authentications/account_activation_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 to_email = form.cleaned_data.get('email')
#                 email = EmailMessage(
#                     subject, message, to=[to_email]
#                 )
#                 email.send()
#                 messages.success(request, 'Please Confirm your email to complete registration.')
#                 messages.success(request, 'we sent you email', 'success')
#
#             elif form.cleaned_data['phone_number']:
#                 random_code = random.randint(1000, 9999)
#                 send_otp_code(form.cleaned_data['phone_number'], random_code)
#                 OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
#                 request.session['user_registration_info'] = {
#                     'username': form.cleaned_data['username'],
#                     'phone_number': form.cleaned_data['phone_number'],
#                     'email': form.cleaned_data['email'],
#                     'first_name': form.cleaned_data['first_name'],
#                     'last_name': form.cleaned_data['last_name'],
#                     'country': form.cleaned_data['country'],
#                     'birthdate': form.cleaned_data['birthdate'],
#                     'password': form.cleaned_data['password'],
#                     'gender': form.cleaned_data['gender'],
#                 }
#                 messages.success(request, 'we sent you a code', 'success')
#                 return redirect('verify_code')
#             return render(request, 'authentications/register.html', {'forms': form})
#
#         else:
#             messages.error(request, 'register failed')
#             return redirect('logout')
#
#
# class ActivateAccount(View):
#
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#             print('ghabl as if')
#         if user is not None and account_activation_token.check_token(user, token):
#             print('ghabl as active')
#             user.is_active = True
#             user.username += '@eml.com'
#             # user.profile.email_confirmed = True
#             user.save()
#             login(request, user)
#             messages.success(request, ('Your account have been confirmed.'))
#
#             return redirect('mail_page:home')
#         else:
#             messages.warning(request, ('The confirmation link was invalid, possibly because it has already
#             been used.'))
#             return redirect('mail_page:home')
#
#
# class UserRegisterVerifyCodeView(View):
#     form_class = VerifyCodeForm
#
#     def get(self, request):
#         form = self.form_class
#         return render(request, 'users/verify.html', {'forms': form})
#
#     def post(self, request):
#         user_session = request.session['user_registration_info']
#         code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#
#             print('*******************************************************************')
#             # print(user)
#             print('*******************************************************************')
#             if cd['code'] == code_instance.code:
#                 User.objects.create_user(user_session['password'],
#                                          username=user_session['username'],
#                                          phone_number=user_session['phone_number'],
#                                          first_name=user_session['first_name'],
#                                          last_name=user_session['last_name'],
#                                          birthdate=user_session['birthdate'],
#                                          gender=user_session['gender'],
#                                          country=user_session['country'])
#                 print('*********************************************************')
#                 print(user_session['username'])
#                 # print(CustomUser.objects.get(user_session['username']))
#                 print('filter', User.objects.filter(username=user_session['username']))
#                 print('*********************************************************')
#                 user = User.objects.get(phone_number=user_session['phone_number'])
#                 user.is_active = True
#                 user.username += '@email.com'
#                 user.save()
#                 # folders = ['inbox', 'sentbox', 'trash', 'draft']
#                 # for folder in folders:
#                 #     email_place_holder = EmailPlaceHolders()
#                 #     email_place_holder.place_holder = folder
#                 #     email_place_holder.save()
#                 # CustomUser.save()
#
#                 code_instance.delete()
#                 messages.success(request, 'you registered.', 'success')
#                 return redirect("email_view")
#             else:
#                 messages.error(request, 'this code is wrong', 'danger')
#                 return redirect('verify_code')
#
#
# # class LogoutView(LoginRequiredMixin, View):
# #     def get(self, request):
# #         logout(request)
# #         messages.success(request, 'you logged out successfully', 'success')
# #         return redirect('login')
#
# def logout(request):
#     # logout(request)
#     return redirect('login')
