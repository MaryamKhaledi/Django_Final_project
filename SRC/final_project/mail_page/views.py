from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from accounts.models import User
from .forms import ComposeForm, ReplyForm, NewContactForm, NewLabelForm
from .models import Email, Contacts, Label


# User.objets.filter(Q(email__isnull=True)|Q(username__isnull=True))


def home(request):
    return render(request, 'mail_page/home.html')


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
            new_email.receiver = get_object_or_404(User, username=cd['receiver'])
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
        return render(request, 'mail_page/home.html',
                      {'username': username, 'all_emails': received, 'all_cc_emails': all_cc_emails,
                       'all_bcc_emails': username_mail_bcc})


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
        sent = Email.objects.filter(user=username)
        return render(request, 'mail_page/sent.html', {'sent': sent})


class DetailEmail(View):
    def get(self, request, id):
        email = Email.objects.get(pk=id)
        # global indexemailid
        # indexemailid = email.id
        return render(request, 'mail_page/detail.html', {'email': email})


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

    return render(request, 'mail_page/reply.html', {'form': form})


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


class ShowContacts(LoginRequiredMixin, View):
    def get(self, request):
        owner = request.user  # this is email username
        print('****', owner)
        contacts = Contacts.objects.filter(owner=owner)
        return render(request, 'mail_page/showcontacts.html', {'contacts': contacts})


class NewContacts(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = NewContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/newcontact.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            newcontact = form.save(commit=False)
            cd = form.cleaned_data
            email = get_object_or_404(User, username=cd['email'])
            # new_contact.user = user
            # rcv = Email.objects.filter(receiver__name__in=receiver)
            owner = request.user
            # Contacts.objects.create(name=cd['name'], email=cd['email'], phone_number=cd['phone_number'],
            # birth_date=cd['birth_date'])
            newcontact.owner = owner
            form.save()
            messages.success(request, 'you created a new email', 'success')
            return redirect('mail_page:showcontacts')
        return render(request, 'mail_page/newcontact.html', {'form': form})


class DetailContacts(View):
    def get(self, request, id):
        contact = Contacts.objects.get(pk=id)
        return render(request, 'mail_page/detailcantacts.html', {'contact': contact})


class DeleteContacts(LoginRequiredMixin, View):
    def get(self, request, id):
        contact = get_object_or_404(Contacts, pk=id)
        if contact.owner == request.user:
            contact.delete()
            messages.success(request, 'contact deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this contact', 'danger')
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
        return render(request, 'mail_page/newcontact.html', {'form': form})

    def post(self, request, *args, **kwargs):
        contact = self.contact_instance
        form = self.form_class(request.POST, instance=contact)
        if form.is_valid():
            new_contact = form.save(commit=False)
            cd = form.cleaned_data
            email = get_object_or_404(User, username=cd['email'])
            owner = request.user
            new_contact.owner = owner
            new_contact.save()
            messages.success(request, 'you updated this post', 'success')
            return redirect('mail_page:detailcontacts', contact.id)


class NewLabel(LoginRequiredMixin, View):
    """New email compose class"""
    form_class = NewLabelForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'mail_page/newlabel.html', {'form': form})

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
            form.save()
            messages.success(request, 'you created a new label', 'success')
            return redirect('mail_page:showlabel')
        return render(request, 'mail_page/newlabel.html', {'form': form})


class ShowLabel(LoginRequiredMixin, View):
    def get(self, request):
        owner = request.user  # this is username
        # label = request.label
        # labelid = label.id
        # print('*****', owner)
        # print('*****', owner.id)
        labels = Label.objects.filter(owner=owner)
        return render(request, 'mail_page/showlabel.html', {'labels': labels})


class LabelEmail():
    pass

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