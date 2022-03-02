from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User
from .forms import ComposeForm
from .models import Email


def home(request):
    return HttpResponseRedirect(f'You are welcome')


class ComposeEmail(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = ComposeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/compose.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_email = form.save(commit=False)
            # new_email.user = request.user
            user = User.objects.get(id=request.user.id)
            new_email.user = user
            # rcv = Email.objects.filter(receiver__name__in=receiver)
            new_email.save()
            messages.success(request, 'you created a new email', 'success')
            return redirect('mail_page:home')


# class ComposeEmail(LoginRequiredMixin, View):
#     form_class = ComposeForm
#
#     def get(self, request):
#         form = self.form_class
#         return render(request, 'mail_page/compose.html', {'form': form})
#
#     def post(self, request, pk):
#         form = self.form_class(request.POST, request.FILES)
#         # fields = ['receiver', 'subject', 'cc', 'bcc', 'body', 'file', 'signature', 'timestamp']
#         if form.is_valid():
#             cd = form.cleaned_data
#             receiver = User.objects.filter(username__in=cd)
#             new_mail = Email.objects.create(subject=cd['subject'], body=cd['body'],
#                                             file=cd['file'])
#             new_mail.cc.set(receiver)
#             new_mail.bcc.set(receiver)
#             messages.success(request, f'email created successfully', 'success')
#         else:
#             messages.error(request, f'The email account you tried to access does not exist. Please check recipient '
#                                     f'email again.', 'error')
#
#         return render(request, 'mail_page/home.html', {'form': form})


class Inbox(LoginRequiredMixin, View):
    """ Email Inbox class """

    def get(self, request):
        # userid = request.user
        # username = User.objects.get(pk=userid)
        username = request.user.username
        print(username)
        received = Email.objects.filter(receiver=username)
        username_mail_cc = Email.objects.filter(cc=username).values()
        username_mail_bcc = Email.objects.filter(bcc=username).values()
        received_mail_cc = received.union(username_mail_cc)
        all_cc_emails = received_mail_cc.union(received_mail_cc)
        return render(request, 'mail_page/inbox.html',
                      {'username': username, 'all_emails': received, 'all_cc_emails': all_cc_emails,
                       'all_bcc_emails': username_mail_bcc})


class SentEmail(View, LoginRequiredMixin):
    def get(self, request, pk):
        username = User.objects.get(pk=pk)
        sent = Email.objects.filter(signature=username).values()
        return render(request, 'mail_page/sent.html', {'sent': sent})
