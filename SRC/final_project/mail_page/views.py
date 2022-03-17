import csv
import json

import username
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from .forms import ComposeForm, ReplyForm, NewContactForm, NewLabelForm, ForwardForm, SearchForm, \
    NewSignatureForm, FilterForm
from .models import Email, Contacts, Label, Signature


# User.objets.filter(Q(email__isnull=True)|Q(username__isnull=True))


# def home(request):
#     return render(request, 'mail_page/home.html', {'username': request.user})


def cc_bcc(cc, bcc):
    all_receiver = []
    if cc is not None:
        cc_list = cc.split(',')
        all_receiver.extend(cc_list)
    if bcc is not None:
        bcc_list = bcc.split(',')
        all_receiver.extend(bcc_list)
    return all_receiver


class ComposeEmail(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = ComposeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/compose.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if "compose" in request.POST:
                cd = form.cleaned_data
                cc_bcc_list = cc_bcc(cd['cc'], cd['bcc'])
                if cd['receiver'] is not None:
                    cc_bcc_list.append(cd['receiver'])
                receiver_list = list(dict.fromkeys(cc_bcc_list))  # pak kardan tekrariha
                if len(receiver_list) == 0:
                    messages.warning(request, 'message not sent(receiver,bcc,cc=none)', 'warning')
                    return redirect('mail_page:home')
                else:
                    for rec in receiver_list:
                        if cd['cc'] is not None and rec in cd['cc']:
                            cd['body'] += "\n sent to: " + rec
                        exist_rec = User.objects.filter(username=rec.strip())
                        if exist_rec:
                            user = User.objects.get(id=request.user.id)
                            cd['user'] = user
                            cd['receiver'] = rec.strip()
                            cd['is_draft'] = False
                            if cd['status'] == 'add signature':
                                sig = Signature.objects.filter(owner=request.user)
                                if sig is not None:
                                    sig = sig[0]  # todo: handel
                                    if sig:
                                        cd['body'] += "\n signature: " + sig.title
                            elif cd['status'] == 'none':
                                sig = None
                            Email.objects.create(user=cd['user'], subject=cd['subject'], body=cd['body'],
                                                 signature=sig,
                                                 receiver=cd['receiver'], file=cd['file'], is_draft=cd['is_draft'])
                    messages.success(request, 'email has sent successfully', 'success')
                    # else:
                    #     messages.warning(request, 'you created a new email', 'warning')
                    return redirect('mail_page:home')
            elif "createdraft" in request.POST:
                cd = form.cleaned_data
                # cc_bcc_list = cc_bcc(cd['cc'], cd['bcc'])
                # cc_bcc_list.append(cd['receiver'])
                # receiver_list = list(dict.fromkeys(cc_bcc_list))
                # for rec in receiver_list:
                #     if cd['cc'] is not None and rec in cd['cc']:
                #         cd['body'] += "\n\n sent to: " + rec
                #     exist_rec = User.objects.filter(username=rec.strip())
                #     if exist_rec:
                user = User.objects.get(id=request.user.id)
                cd['user'] = user  # cd['user']= request.user
                #         cd['receiver'] = rec.strip()
                cd['is_draft'] = True
                Email.objects.create(user=cd['user'], subject=cd['subject'], body=cd['body'],
                                     receiver=cd['receiver'], file=cd['file'], is_draft=cd['is_draft'])
                messages.success(request, 'Email drafted', 'success')
                # else:
                #     messages.warning(request, 'you created a new email', 'warning')
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

class NewSignature(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = NewSignatureForm

    def setup(self, request, *args, **kwargs):
        self.signature_instance = Signature.objects.filter(owner=request.user)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        signature = self.signature_instance
        if signature:
            messages.error(request, 'u already have one signature', 'danger')
            return redirect('mail_page:showsignature')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/newsignature.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            newsignature = form.save(commit=False)
            cd = form.cleaned_data
            owner = request.user
            newsignature.owner = owner
            newsignature.save()
            messages.success(request, 'you created a new signature', 'success')
            return redirect('mail_page:showsignature')
        return render(request, 'mail_page/newsignature.html', {'username': request.user, 'form': form})


class ShowSignature(LoginRequiredMixin, View):
    def get(self, request):
        owner = request.user
        signatures = Signature.objects.filter(owner=owner)
        return render(request, 'mail_page/showsignature.html', {'username': request.user, 'signatures': signatures})


class DeleteSignature(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            signature = get_object_or_404(Signature, pk=id)
            if signature.owner == request.user:
                signature.delete()
                messages.success(request, 'signature deleted successfully', 'success')
            else:
                messages.error(request, 'you cant delete this signature', 'danger')
        except:
            pass
        return redirect('mail_page:showsignature')


class Inbox(LoginRequiredMixin, View):
    """ Email Inbox class """

    def get(self, request):
        perfect_email = 0
        username = request.user
        received = Email.objects.filter(
            (Q(is_trash=False) & Q(is_archived=False) & Q(is_draft=False)) & Q(receiver=username))
        for i in received:
            t1 = int(i.timestamp.timestamp())
            t2 = int(timezone.now().timestamp())
            if 10 >= t2 - t1 >= 0:
                perfect_email += 1
        if perfect_email != 0:
            messages.success(request, f'u have {perfect_email} new messages', 'success')

        return render(request, 'mail_page/home.html', {'username': username, 'all_emails': received})


# class ReplyView(LoginRequiredMixin, View):
#     form_class = ReplyForm
#
#     def post(self, request, email_id):
#         email = get_object_or_404(Email, id=email_id)
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             reply = form.save(commit=False)
#             reply.user = request.user
#             reply.reply = email
#             reply.is_reply = True
#             reply.save()
#             messages.success(request, 'your reply submitted successfully', 'success')
#         return redirect('home', email.id)


class SentEmail(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user
        #  todo: add Q(is_draft=False)
        sent = Email.objects.filter((Q(is_trash=False) & Q(is_archived=False)) & Q(user=username))
        return render(request, 'mail_page/sent.html', {'username': username, 'sent': sent})


class DraftBox(LoginRequiredMixin, View):
    def get(self, request):
        draft = Email.objects.filter(is_draft=True, user=request.user)
        return render(request, 'mail_page/draftbox.html', {'username': request.user, 'draft': draft})


# class DetailDraft(LoginRequiredMixin, View):
#     form_class = ComposeForm
#
#     def setup(self, request, *args, **kwargs):
#         self.draft_instance = get_object_or_404(Email, pk=kwargs['id'])
#         return super().setup(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         draft = self.draft_instance
#         form = self.form_class(instance=draft)
#         return render(request, 'mail_page/compose.html', {'username': request.user, 'form': form})
#
#     def post(self, request, *args, **kwargs):
#         draft = self.draft_instance
#         form = self.form_class(request.POST, instance=draft)
#         if form.is_valid():
#             new_email = form.save(commit=False)
#             cd = form.cleaned_data
#             new_email.user = request.user
#             new_email.save()
#             messages.success(request, 'you updated this post', 'success')
#             return redirect('mail_page:draftbox')


class DetailDraft(LoginRequiredMixin, View):
    form_class = ComposeForm

    def setup(self, request, *args, **kwargs):
        self.draft_instance = get_object_or_404(Email, pk=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        draft = self.draft_instance
        form = self.form_class(instance=draft)
        return render(request, 'mail_page/compose.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        draft = self.draft_instance
        form = self.form_class(request.POST, instance=draft)
        if form.is_valid():
            if "compose" in request.POST:
                cd = form.cleaned_data
                cc_bcc_list = cc_bcc(cd['cc'], cd['bcc'])
                if cd['receiver'] is not None:
                    cc_bcc_list.append(cd['receiver'])
                receiver_list = list(dict.fromkeys(cc_bcc_list))
                for rec in receiver_list:
                    if cd['cc'] is not None and rec in cd['cc']:
                        cd['body'] += "\n sent to: " + rec
                    exist_rec = User.objects.filter(username=rec.strip())
                    if exist_rec:
                        user = User.objects.get(id=request.user.id)
                        cd['user'] = user
                        cd['receiver'] = rec.strip()
                        cd['is_draft'] = False
                        Email.objects.create(user=cd['user'], subject=cd['subject'], body=cd['body'],
                                             receiver=cd['receiver'], file=cd['file'], is_draft=cd['is_draft'])
                        draft_email = Email.objects.get(pk=kwargs['id'])
                        draft_email.delete()
                        messages.success(request, 'you created a new email', 'success')
                return redirect('mail_page:home')
            elif "createdraft" in request.POST:
                cd = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                cd['user'] = user
                cd['is_draft'] = True
                Email.objects.create(user=cd['user'], subject=cd['subject'], body=cd['body'],
                                     receiver=cd['receiver'], file=cd['file'], is_draft=cd['is_draft'])
                messages.success(request, 'Email drafted', 'success')
            return redirect('mail_page:home')


class CreateDraft(LoginRequiredMixin, View):
    form_class = ComposeForm

    def get(self, request, id):
        form = self.form_class
        return render(request, 'mail_page/compose.html', {'form': form})

    def post(self, request, id):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            draft_email = form.save(commit=False)
            draft_email.user = request.user
            draft_email.save()
            messages.success(request, 'email drafted', 'success')
            return redirect('mail_page:home')


class DetailEmail(LoginRequiredMixin, View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        # global indexemailid
        # indexemailid = email.id
        return render(request, 'mail_page/detail.html', {'username': request.user, 'email': email})


# class ReplyEmail(View):
#     form_class = ReplyForm
#
#     def get(self, request, email_id):
#         form = self.form_class
#         return render(request, 'mail_page/reply.html', {'form': form})
#
#     def post(self, request, email_id):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             reply_email = form.save(commit=False)
#             # reply_email.resiver = indexemailid.user
#             sent = Email.objects.filter(id=email_id)
#             reply_email.user = request.user.username
#             reply_email.receiver = sent.user
#             reply_email.save()
#             messages.success(request, 'your reply email submitted successfully', 'success')
#             return render(request, 'mail_page/reply.html', {'form': form})


def reply_email(request, email_user):
    # sent = Email.objects.get(id=email_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply_email = form.save(commit=False)
            reply_email.user = request.user
            reply_email.receiver = email_user
            reply_email.save()
            messages.success(request, 'your reply email submitted successfully', 'success')
            return redirect('mail_page:home')
    else:
        form = ReplyForm()

    return render(request, 'mail_page/reply.html', {'username': request.user, 'form': form})


class ForwardEmail(LoginRequiredMixin, View):
    # sent = Email.objects.get(id=email_id)
    form_class = ForwardForm

    def get(self, request, id):
        form = self.form_class
        return render(request, 'mail_page/forward.html', {'username': request.user, 'form': form})

    def post(self, request, id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # base_mail = form.save(commit=False)
            mail = Email.objects.get(pk=id)
            # todo: multiple receptions
            cd['subject'] = mail.subject
            cd['body'] = mail.body
            cd['file'] = mail.file
            cd['timestamp'] = timezone.now()
            cd['user'] = request.user
            cc_bcc_list = cc_bcc(cd['cc'], cd['bcc'])
            if cd['receiver'] is not None:
                cc_bcc_list.append(cd['receiver'])
            receiver_list = list(dict.fromkeys(cc_bcc_list))
            for rec in receiver_list:
                if cd['cc'] is not None and rec in cd['cc']:
                    cd['body'] += "\n\n sent to: " + rec
                exist_rec = User.objects.filter(username=rec.strip())
                if exist_rec:
                    cd['receiver'] = rec.strip()
                    Email.objects.create(user=cd['user'], subject=cd['subject'], body=cd['body'], file=cd['file']
                                         , receiver=cd['receiver'])
                    # base_mail.save()
                    messages.success(request, 'Forwarded successfully', 'success')
            return redirect('mail_page:sent')


# @method_decorator(login_required)
# def post(self, request, *args, **kwargs):
#     form = self.form_class(request.POST)
#     if form.is_valid():
#         new_comment = form.save(commit=False)
#         new_comment.user = request.user
#         new_comment.post = self.post_instance
#         new_comment.save()
#         messages.success(request, 'your comment submitted successfully', 'success')
#         return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)

#  todo : class emailcontact be dalile adam neshon dadane resiver be moshkel khord

class EmailContact(LoginRequiredMixin, View):
    form_class = ReplyForm

    def get(self, request, id):
        form = self.form_class
        return render(request, 'mail_page/contactemail.html', {'username': request.user, 'form': form})

    def post(self, request, id):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            contact_email = form.save(commit=False)
            contact_object = Contacts.objects.get(pk=id, owner=request.user.id)
            contact_email.user = request.user
            contact_email.receiver = contact_object.email
            contact_email.save()
            messages.success(request, 'your email sent successfully', 'success')
            return redirect('mail_page:showcontacts')

        return render(request, 'mail_page/contactemail.html', {'username': request.user, 'form': form})


# def emailcontct(request, id):
#     if request.method == 'POST':
#         form = ReplyForm(request.POST, request.FILES)
#         if form.is_valid():
#             contact_email = form.save(commit=False)
#             contact_object = Contacts.objects.get(pk=id)
#             print(contact_object.id)
#             contact_email.user = request.user
#             contact_email.receiver = contact_object.email
#             contact_email.save()
#             messages.success(request, 'your reply email submitted successfully', 'success')
#             return redirect('mail_page:home')
#     else:
#         form = ReplyForm()
#
#     return render(request, 'mail_page/reply.html', {'form': form})


class ShowContacts(LoginRequiredMixin, View):
    def get(self, request):
        owner = request.user  # this is email username
        contacts = Contacts.objects.filter(owner=owner)
        form = SearchForm()
        if 'search' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                contacts = contacts.filter(Q(name__icontains=cd) | Q(email__icontains=cd))
        return render(request, 'mail_page/showcontacts.html',
                      {'username': request.user, 'form': form, 'contacts': contacts})


# @method_decorator(login_required)
def contact_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    writer = csv.writer(response)
    allcontacts = Contacts.objects.filter(owner=request.user)
    writer.writerow(['Name', 'Email', 'Phone_number', 'Other_email', 'Birth_date', 'Owner'])
    for venue in allcontacts:
        writer.writerow([venue.name, venue.email, venue.phone_number, venue.other_email, venue.birth_date, venue.owner])
    return response


# def contact_csv(request):
#     contacts = Contacts.objects.filter(owner=request.user)
#     # return HttpResponse(contacts)
#     response = HttpResponse('text/csv')
#     response['Content-Disposition'] = 'attachment; filename=contacts.csv'
#     writer = csv.writer(response)
#     writer.writerow(['Name', 'Email', 'Phone_number', 'Other_email', 'Birth_date', 'owner'])
#     studs = contacts.values_list('name', 'email', 'phone_number', 'other_email', 'owner')
#     for std in studs:
#         writer.writerow(std)
#     return response


class NewContacts(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = NewContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/newcontact.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            newcontact = form.save(commit=False)
            cd = form.cleaned_data
            try:
                # noinspection PyBroadException
                email = get_object_or_404(User, username=cd['email'])
                owner = request.user
                newcontact.owner = owner
                form.save()
                messages.success(request, f'You Add {cd["name"]} in your contact', 'success')
            except:
                # todo : sms monaseb
                messages.warning(request, 'email not found !', 'warning')
                return redirect('mail_page:newcontact')
        return redirect('mail_page:showcontacts')


class DetailContacts(View):
    def get(self, request, id):
        contact = Contacts.objects.get(pk=id)
        return render(request, 'mail_page/detailcontacts.html', {'username': request.user, 'contact': contact})


class DeleteContacts(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            contact = get_object_or_404(Contacts, pk=id)
            if contact.owner == request.user:
                contact.delete()
                messages.success(request, 'contact deleted successfully', 'success')
            else:
                messages.error(request, 'you cant delete this contact', 'danger')
        except:
            pass
        return redirect('mail_page:showcontacts')


class UpdateContacts(LoginRequiredMixin, View):
    form_class = NewContactForm

    def setup(self, request, *args, **kwargs):
        self.contact_instance = get_object_or_404(Contacts, pk=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        contact = self.contact_instance
        if not contact.owner == request.user:
            messages.error(request, 'you cant update this contact', 'danger')
            return redirect('mail_page:showcontacts')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        contact = self.contact_instance
        form = self.form_class(instance=contact)
        return render(request, 'mail_page/newcontact.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        contact = self.contact_instance
        form = self.form_class(request.POST, instance=contact)
        if form.is_valid():
            new_contact = form.save(commit=False)
            cd = form.cleaned_data
            email = get_object_or_404(User, username=cd['email'])
            new_contact.owner = request.user
            new_contact.save()
            messages.success(request, 'you updated this post', 'success')
            return redirect('mail_page:detailcontacts', contact.id)


class NewLabel(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = NewLabelForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/newlabel.html', {'username': request.user, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            newlabel = form.save(commit=False)
            cd = form.cleaned_data
            # email = get_object_or_404(User, username=cd['email'])
            # new_contact.user = user
            # rcv = Email.objects.filter(receiver__name__in=receiver)
            owner = request.user
            # Contacts.objects.create(name=cd['name'], email=cd['email'], phon_number=cd['phon_number'],
            # birth_date=cd['birth_date'])
            newlabel.owner = owner
            newlabel.save()
            messages.success(request, 'you created a new label', 'success')
            return redirect('mail_page:showlabel')
        return render(request, 'mail_page/newlabel.html', {'username': request.user, 'form': form})


class ShowLabel(LoginRequiredMixin, View):
    def get(self, request):
        owner = request.user  # this is username
        # label = request.label
        # labelid = label.id
        # print('*****', owner)
        # print('*****', owner.id)
        labels = Label.objects.filter(owner=owner)
        return render(request, 'mail_page/showlabel.html', {'username': request.user, 'labels': labels})


class AddLabel(LoginRequiredMixin, View):
    form_class = NewLabelForm

    def get(self, request, id):
        form = self.form_class
        return render(request, 'mail_page/addlabel.html', {'username': request.user, 'form': form})

    def post(self, request, id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                new_label = form.save(commit=False)
                label_t = Label.objects.get(title=cd["title"])
                # for id in list_id:
                email = Email.objects.get(pk=id)
                email.label.add(label_t)
                email.save()
                return redirect('mail_page:detail')
            except:
                return redirect('mail_page:home')


class LabelDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        email_list = []
        label = Label.objects.get(pk=id)
        labels_email = label.email_set.all().values_list('id')
        labels_list = list(labels_email)
        for i in labels_list:
            email = Email.objects.get(pk=i[0])
            email_list.append(email)
        # print(labels_email['id'])
        # email_id = labels_email['id']
        # email = Email.objects.get(pk=email_id)
        return render(request, 'mail_page/labeldetail.html',
                      {'username': request.user, 'all_emails': email_list, 'label': label})


class DeleteLabel(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            label = get_object_or_404(Label, pk=id)
            if label.owner == request.user:
                label.delete()
                messages.success(request, 'label deleted successfully', 'success')
            else:
                messages.error(request, 'you cant delete this label', 'danger')
        except:
            pass
        return redirect('mail_page:showlabel')


# class UserContactView(LoginRequiredMixin, View):
#     form_class = AddContact
#     template_name = 'users/add_contact.html'
#
#     def get(self, request):
#         form = self.form_class
#         return render(request, self.template_name, {'forms': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             new_contact = form.save(commit=False)
#             new_contact.owner_contact = request.user
#             new_contact.save()
#             messages.success(request, f'You Add {cd["name"]} in your contact', 'success')
#             return redirect('email_view')
#
#
# class ShowAllContact(LoginRequiredMixin, View):
#     template = 'users/all_contact.html'
#
#     def get(self, request):
#         all_contact = Contact.objects.filter(owner_contact=request.user.id)
#         return render(request, self.template, {"all_contact": all_contact})
#
#
# class DetailContactView(LoginRequiredMixin, View):
#     template = 'users/detail_contact.html'
#
#     def setup(self, request, *args, **kwargs):
#         self.email_instance = get_object_or_404(Contact, pk=kwargs['contact_id'])
#         return super().setup(request, *args, **kwargs)
#
#     def get(self, request, contact_id):
#         contact = Contact.objects.get(pk=contact_id)
#         return render(request, self.template, {'contact': contact})
#
#
# class Update(LoginRequiredMixin, View):
#     form_class = AddContact
#     template = 'users/update_contact.html'
#
#     def setup(self, request, *args, **kwargs):
#         self.contact_instance = Contact.objects.get(pk=kwargs["contact_id"])
#         return super().setup(request, *args, **kwargs)
#
#     # def dispatch(self, request, *args, **kwargs):
#     #     conatct= self.contact_instance
#     #     if not conatct.user.id == request.user.id:
#     #         messages.error(request, 'you can not edit', 'danger')
#     #         return redirect('home')
#     #     return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         conatct = self.contact_instance
#         form = self.form_class(instance=conatct)
#         return render(request, self.template, {'forms': form})
#
#     def post(self, request, *args, **kwargs):
#         conatct = self.contact_instance
#         form = self.form_class(request.POST, instance=conatct)
#         if form.is_valid():
#             update_conatct = form.save(commit=False)
#             update_conatct.owner_contact = request.user
#             update_conatct.save()
#             messages.success(request, "updated post", 'success')
#             return redirect('detail_contact', update_conatct.id)
#
#
# class ContactDelete(LoginRequiredMixin, View):
#     def get(self, request, contact_id):
#         contact = Contact.objects.get(pk=contact_id)
#         contact.delete()
#         messages.success(request, "delete was successfully", 'success')
#         return redirect('email_view')
#
#
# def export_contact_csv(request):
#     contacts = Contact.objects.filter(owner_contact=request.user)
#     # return HttpResponse(contacts)
#     response = HttpResponse('text/csv')
#     response['Content-Disposition'] = 'attachment; filename=contacts.csv'
#     writer = csv.writer(response)
#     writer.writerow(['ID', 'owner_contact', 'phone', 'Name', 'Email', 'Birthdate'])
#     studs = contacts.values_list('id', 'owner_contact', 'phone', 'name', 'email', 'birthdate')
#     for std in studs:
#         writer.writerow(std)
#     return response

class Trash(LoginRequiredMixin, View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        if email.is_trash is False:
            email.is_trash = True
            # print(email.is_trash)
            # email.save(update_fields=['is_trash'])
            # # email.update()
            # print(email.is_trash)
        else:
            email.is_trash = False

        email.save(update_fields=['is_trash'])
        return redirect('mail_page:trashbox')


class TrashBox(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user
        emails = Email.objects.filter((Q(receiver=username) | Q(user=username)) & Q(is_trash=True))
        return render(request, 'mail_page/trashbox.html', {'username': request.user, 'emails': emails})


class Archive(LoginRequiredMixin, View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        if email.is_archived is False:
            email.is_trash = False
            email.is_archived = True
            # print(email.is_trash)
            # email.save(update_fields=['is_trash'])
            # # email.update()
            # print(email.is_trash)
        else:
            email.is_archived = False

        email.save(update_fields=['is_archived'])
        return redirect('mail_page:archivebox')


class ArchiveBox(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user
        emails = Email.objects.filter((Q(receiver=username) | Q(user=username)) & (Q(is_trash=False) &
                                                                                   Q(is_archived=True)))

        return render(request, 'mail_page/archivebox.html', {'username': request.user, 'emails': emails})


class DeleteEmail(LoginRequiredMixin, View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        email.delete()
        messages.success(request, "email has deleted successfully FOREVER!!", 'success')
        return redirect('mail_page:trashbox')


# def search_email(request):
#     if request.method == 'POST':
#         search_str = json.loads(request.body).get('searchText')
#         expenses = Email.objects.filter(
#             receiver__icontains=search_str, owner=request.user) | Email.objects.filter(
#             subject__icontains=search_str, owner=request.user) | Email.objects.filter(
#             body__icontains=search_str, owner=request.user) | Email.objects.filter(
#             timestamp__istartswith=search_str, owner=request.user)
#
#         date = expenses.values()
#         return JsonResponse(list(date), safe=False)


class FilterEmail(LoginRequiredMixin, View):  # todo: action
    form_class = FilterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'mail_page/filter.html', {'username': request.user, 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            emails = Email.objects.filter(receiver=request.user)
            if cd['sender']:
                try:
                    sender = User.objects.get(username=cd['sender'])
                    emails = emails.filter(user=sender.id)
                except:
                    messages.warning(request, "this user does not exist", 'danger')
                    return redirect('mail_page:filteremail')
            if cd['subject']:
                emails = emails.filter(Q(subject__icontains=cd['subject']))
            if cd['body']:
                emails = emails.filter(Q(body__icontains=cd['body']))
            if cd['file'] == True:
                emails = emails.filter(~Q(file=''))
            for email in emails:
                if cd['action'] == 'trash':
                    trash = Trash()
                    trash.get(request, email.id)
                elif cd['action'] == 'archive':
                    archive = Archive()
                    archive.get(request, email.id)
                elif cd['action'] == 'label':
                    label = AddLabel()
                    label.post(request, email.id)
                else:
                    pass
            return render(request, 'mail_page/showfilteremail.html', {'username': request.user, 'emails': emails})
        return render(request, 'mail_page/filter.html', {'username': request.user, 'form': form})


# @method_decorator(csrf_exempt)
class FilterAlpineJs(View):

    def post(self, request):
        text = self.request.POST.get('search', None)
        email_list = []
        if text:
            emails = Email.objects.filter(Q(receiver=request.user) | Q(user=request.user))
            if emails is not None:
                emails = emails.filter(Q(subject__icontains=text) | Q(receiver__icontains=text)
                                       | Q(body__icontains=text) | Q(user__username__icontains=text))
            email_list = [{
                'id': email.id,
                'subject': email.subject,
                'user': email.user.username,
                'receiver': email.receiver} for email in emails]

        return HttpResponse(json.dumps({'list': email_list}))
