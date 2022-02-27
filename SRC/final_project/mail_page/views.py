from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
# from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User
from .forms import EmailForm
from .models import Email
from django.views.generic import ListView, DetailView
from django.core import mail


def home(request, pk):
    # render(request, 'mail_page/load.html', {'pk':pk})
    return HttpResponse(f"{pk}'re welcome")


class ComposeEmail(View):
    form_class = EmailForm

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        # fields = ['receiver', 'subject', 'cc', 'bcc', 'body', 'file', 'signature', 'timestamp']
        if form.is_valid():
            cd = form.cleaned_data
            Email.objects.create(subject=cd['subject'], cc=cd['cc'], bcc=cd['bcc'], body=cd['body'],
                                 created=cd['file'], signature=cd['signature'], timestamp=['timestamp'])
            messages.success(request, f'todo created successfully', 'success')

        return render(request, 'mail_page/compose.html', {'form': form})


class Inbox(View, LoginRequiredMixin):
    def get(self, request, pk):
        username = User.objects.get(pk=pk)
        received = Email.objects.filter(receiver=username).values()
        username_mail_cc = Email.objects.filter(cc=username).values()
        username_mail_bcc = Email.objects.filter(bcc=username).values()
        received_mail_cc = received.union(username_mail_cc)
        all_emails = received_mail_cc.union(received_mail_cc)
        return render(request, 'mail_page/inbox.html', {'user_id': pk, 'username': username, 'all_emails': all_emails})


class SentEmail(View, LoginRequiredMixin):
    def get(self, request, pk):
        username = User.objects.get(pk=pk)
        sent = Email.objects.filter(signature=username).values()
        return render(request, 'mail_page/sent.html', {'sent': sent})
