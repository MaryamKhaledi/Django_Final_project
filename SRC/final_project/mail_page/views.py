from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
# from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import render, redirect
from django.views import View
from accounts.models import User
from .forms import NewEmailForm
from .models import Email
from django.views.generic import ListView, DetailView
from django.core import mail


def home(request):
    return HttpResponseRedirect(f'You are welcome')


# class ComposeEmail(LoginRequiredMixin, View):
#     # resiver moshakhas nist
#     form_class = NewEmailForm
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class
#         return render(request, 'mail_page/compose.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             new_email = form.save(commit=False)
#             new_email.sender = request.sender
#             new_email.signature = request.sender
#             # new_email.timestamp = request.timezone.now()
#             new_email.save()
#         messages.success(request, 'you created a new email', 'success')
#         return redirect('mail_page:home', new_email.id)


class ComposeEmail(LoginRequiredMixin, View):
    form_class = NewEmailForm

    def get(self, request):
        form = self.form_class
        return render(request, 'mail_page/compose.html', {'form': form})

    def post(self, request, pk):
        form = self.form_class(request.POST, request.FILES)
        # fields = ['receiver', 'subject', 'cc', 'bcc', 'body', 'file', 'signature', 'timestamp']
        if form.is_valid():
            cd = form.cleaned_data
            receiver = User.objects.filter(username__in=cd)
            new_mail = Email.objects.create(subject=cd['subject'], body=cd['body'],
                                            file=cd['file'])
            new_mail.cc.set(receiver)
            new_mail.bcc.set(receiver)
            messages.success(request, f'todo created successfully', 'success')
        else:
            messages.error(request, f'The email account you tried to access does not exist. Please check recipient '
                                    f'email again.', 'error')

        return render(request, 'mail_page/home.html', {'form': form})


class PostCreateView(LoginRequiredMixin, View):
    form_class = NewEmailForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_email = form.save(commit=False)
            new_email.sender = request.sender
            new_email.save()
            messages.success(request, 'you created a new post', 'success')
            return redirect('home:post_detail', new_email.id)


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
