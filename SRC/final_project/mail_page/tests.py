from django.db.models import Q
from django.test import TestCase
from .forms import *
from .models import *
from accounts.models import *
from django.urls import reverse_lazy
from django.urls import reverse
from django.test import Client


# Create your tests here.
class MailPageTest(TestCase):
    def setup(self):
        self.client = Client()
        user1 = User.objects.create(username="ellyyy@eml.com", password=12345678, is_active=True)
        user2 = User.objects.create(username="melika@eml.com", password=87654321, is_active=True)
        user3 = User.objects.create(username="mary@eml.com", password=87654320, is_active=True)
        email = Email.objects.create(user=user1, receiver="melika@eml.com", cc=user3.username, bcc=user1.username,
                                     status="none")

    def test_compose(self):
        form = ComposeForm(
            data={'receiver=': "melika@eml.com", "cc": "", "bcc": "", "subject": "test test", "body": "hi test zesht",
                  "file": "", "status": "none"})
        self.assertTrue(form.is_valid())

    def test_url_compose(self):
        # user2 = User.objects.create(username="melika@eml.com", password=123456789, is_active=True)
        # self.client.login(username="melika@eml.com", password=123456789)
        login = self.client.login(username="melika@eml.com", password='1X<ISRUkw+tuK')
        response = self.client.get('/mail_page/compose/')
        self.assertEqual(response.status_code, 302)
        # response = self.client.get(reverse_lazy('mail_page:compose'), follow=True)
        # self.assertEqual(response.status_code, 200)

    def test_inbox(self):
        user2 = User.objects.create(username="melika@eml.com", password='87654321', is_active=True)
        email = Email.objects.create(user=user2, receiver="maryamkhanoom@eml.com", status="none")
        received_email = Email.objects.get(receiver="maryamkhanoom@eml.com")
        self.assertEqual(received_email.receiver, "maryamkhanoom@eml.com")

    def test_send(self):
        user1 = User.objects.create(username="maryamkhanoom@eml.com", password='12345678', is_active=True)
        email = Email.objects.create(user=user1, receiver="melika@eml.com", cc="user3.username", bcc=user1.username,
                                     status="none")
        received_email = Email.objects.get(user=user1)
        self.assertEqual(received_email.user.username, "maryamkhanoom@eml.com")

    def test_draft(self):
        user1 = User.objects.create(username="ellyyy@eml.com", password='12345678', is_active=True)
        email = Email.objects.create(user=user1, receiver="melika@eml.com", cc="user3.username", bcc=user1.username,
                                     status="none", is_draft=True)
        received_email = Email.objects.get(user=user1)
        self.assertTrue(received_email.is_draft)

    def test_reply(self):
        form = ReplyForm(data={"subject": "test test", "body": "hi test zesht", "file": "", "status": "none"})
        self.assertTrue(form.is_valid())

    def test_url_reply(self):
        user2 = User.objects.create(username="melika@eml.com", password='87654321', is_active=True)
        email = Email.objects.create(user=user2, receiver="melika@eml.com", status="none")
        email_id = Email.objects.get(pk=email.id)
        response = self.client.get(f'/mail_page/reply/{email_id.id}')
        self.assertEqual(response.status_code, 200)

    def test_forward(self):
        user1 = User.objects.create(username="melika@eml.com", password='12345678', is_active=True)
        form = ForwardForm(data={'receiver': "melika@eml.com", "cc": "", "bcc": "", "status": "none"})
        print(form)
        self.assertTrue(form.is_valid())
        user = User.objects.get(username=form.data['receiver'])
        self.assertEqual("melika@eml.com", user.username)

    def test_url_forward(self):
        user2 = User.objects.create(username="melika@eml.com", password='87654321', is_active=True)
        email = Email.objects.create(user=user2, receiver="melika@eml.com", status="none")
        email_id = Email.objects.get(pk=email.id)
        response = self.client.get(f'/mail_page/forward/{email_id.id}')
        self.assertEqual(response.status_code, 302)

    def test_email_contact(self):
        user1 = User.objects.create(username="melika@eml.com", password='12345678', is_active=True)
        form = ReplyForm(data={'subject': "test contact", 'body': "Hi contact", 'file': "", 'status': "none"})
        self.assertTrue(form.is_valid())
        contact = Contacts.objects.create(name="Maryamaaaa", email="maryamaaaa@eml.com", owner=user1)
        self.assertEqual("melika@eml.com", contact.owner.username)

    def test_show_contacts(self):
        user1 = User.objects.create(username="melika@eml.com", password='12345678', is_active=True)
        form = NewContactForm(data={'name': 'Diarrr', 'email': 'Diarrr@eml.com', 'phone_number': '',
                                    'other_email': '', 'birth_date': ''})
        self.assertTrue(form.is_valid())

    def test_label(self):
        user1 = User.objects.create(username="melika@eml.com", password='12345678', is_active=True)
        form = NewLabelForm(data={'title': 'django_test'})
        self.assertTrue(form.is_valid())

    def test_url_archive(self):
        user2 = User.objects.create(username="melika@eml.com", password='87654321', is_active=True)
        email = Email.objects.create(user=user2, receiver="melika@eml.com", status="none")
        email_id = Email.objects.get(pk=email.id)
        response = self.client.get(f'/mail_page/archive/{email_id.id}')
        self.assertEqual(response.status_code, 302)

    def test_url_trash(self):
        user2 = User.objects.create(username="melika@eml.com", password='87654321', is_active=True)
        email = Email.objects.create(user=user2, receiver="melika@eml.com", status="none")
        email_id = Email.objects.get(pk=email.id)
        response = self.client.get(f'/mail_page/trash/{email_id.id}')
        self.assertEqual(response.status_code, 302)
