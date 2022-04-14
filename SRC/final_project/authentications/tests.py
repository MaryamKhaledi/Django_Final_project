from django.test import TestCase
from .forms import LoginForm, RegisterForm
from accounts.models import User
from django.urls import reverse


class AuthenticationsTest(TestCase):

    def setUp(self):
        user_1 = User.objects.create(username='maryamkhanoom@eml.com', password='ab654321')

    def test_register_form(self):
        form = RegisterForm(
            data={'username': "maryamkhanoom@eml.com", 'password': 'ab654321', 'first_name': '', 'last_name': '',
                  'recovery': 'Phone', 'email': 'math.khaledi7444@gmail.com', 'phone_number': '',
                  'birth_date': '', 'gender': '', 'country': 'Tehran'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.data['password'], 'ab654321')

    def test_login(self):
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)
