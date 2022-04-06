from django.db.models import Q
from django.test import TestCase
from .forms import *
from .models import *
from accounts.models import *


# Create your tests here.
class MailPageTest(TestCase):
    def setup(self):
        user1 = User.objects.create(username="ellyyy@eml.com", password=12345678, is_active=True)
        user2 = User.objects.create(username="melika@eml.com", password=87654321, is_active=True)
        user3 = User.objects.create(username="mary@eml.com", password=87654320, is_active=True)
        email = Email.objects.create(user=user1, receiver="melika@eml.com", cc=user3.username, bcc=user1.username,
                                     status="none")

    # def test_compose(self):
    #     form = ComposeForm(
    #         data={'receiver=': "melika@eml.com", "cc": "", "bcc": "", "subject": "test test", "body": "hi test zesht",
    #               "file": "", "status": "none"})
    #     self.assertTrue(form.is_valid())

    # todo : Signature classes tests + url

    # def test_inbox(self):
    #     user2 = User.objects.create(username="melika@eml.com", password=87654321, is_active=True)
    #     email = Email.objects.create(user=user2, receiver="melika@eml.com",status="none")
    #     received_email = Email.objects.get(receiver="melika@eml.com")
    #     self.assertEqual(received_email.receiver, "melika@eml.com")

    # def test_send(self):
    #     user1 = User.objects.create(username="ellyyy@eml.com", password=12345678, is_active=True)
    #     email = Email.objects.create(user=user1, receiver="melika@eml.com", cc="user3.username", bcc=user1.username,
    #                                  status="none")
    #     received_email = Email.objects.get(user=user1)
    #     self.assertEqual(received_email.user.username, "ellyyy@eml.com")

    # def test_draft(self):
    #     user1 = User.objects.create(username="ellyyy@eml.com", password=12345678, is_active=True)
    #     email = Email.objects.create(user=user1, receiver="melika@eml.com", cc="user3.username", bcc=user1.username,
    #                                  status="none", is_draft=True)
    #     received_email = Email.objects.get(user=user1)
    #     self.assertTrue(received_email.is_draft)

    # def test_reply(self):
    #     form = ReplyForm(
    #             data={"subject": "test test", "body": "hi test zesht",
    #                   "file": "", "status": "none"})
    #     self.assertTrue(form.is_valid())

    # def test_forward(self):
    #     user1 = User.objects.create(username="melika@eml.com", password=12345678, is_active=True)
    #     form = ForwardForm(
    #             data={'receiver': "melika@eml.com", "cc": "", "bcc": "","status": "none"})
    #     print(form)
    #     self.assertTrue(form.is_valid())
    #     userr = User.objects.get(username=form.data['receiver'])
    #     self.assertEqual("melika@eml.com", userr.username)
