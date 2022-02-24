from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from final_project import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token


# Create your views here.
def home(request):
    return render(request, "authentications/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        elif len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        elif password1 != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        elif not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        # accounts.is_active = False
        user.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + user.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_authentications.html', {

            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentications/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        # accounts.profile.signup_confirmation = True
        user.save()
        login(request, user)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views.generic import View, UpdateView
# from django.utils.encoding import force_text
# from .forms import SignUpForm, ProfileForm
# from django.contrib import messages
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.template.loader import render_to_string
# from accounts.models import User
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# # from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode
#
# from .tokens import account_activation_token
# class SignUpView(View):
#     form_class = SignUpForm
#     template_name = 'commons/signup.html'
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             accounts = form.save(commit=False)
#             accounts.is_active = False  # Deactivate account till it is confirmed
#             accounts.save()
#
#             current_site = get_current_site(request)
#             subject = 'Activate Your MySite Account'
#             message = render_to_string('emails/account_activation_email.html', {
#                 'accounts': accounts,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(accounts.pk)),
#                 'token': account_activation_token.make_token(accounts),
#             })
#             accounts.email_user(subject, message)
#
#             messages.success(request, ('Please Confirm your email to complete registration.'))
#
#             return redirect('login')
#
#         return render(request, self.template_name, {'form': form})
#
#
# class ActivateAccount(View):
#
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             accounts = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             accounts = None
#
#         if accounts is not None and account_activation_token.check_token(accounts, token):
#             accounts.is_active = True
#             accounts.profile.email_confirmed = True
#             accounts.save()
#             login(request, accounts)
#             messages.success(request, ('Your account have been confirmed.'))
#             return redirect('home')
#         else:
#             messages.warning(request, ('The confirmation link was invalid, possibly because it has
#             already been used.'))
#             return redirect('home')
#
#
# # Edit Profile View
# class ProfileView(UpdateView):
#     model = User
#     form_class = ProfileForm
#     success_url = reverse_lazy('home')
#     template_name = 'commons/profile.html'
