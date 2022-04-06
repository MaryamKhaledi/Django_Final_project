# from django.urls import reverse_lazy
# from django.urls import reverse
# from django.test import TestCase
# from django.utils import timezone
# from accounts.models import *
#
#
# class AuthenticationsTest(TestCase):
#     def setUp(self):
#         # Create two users
#         test_user1 = User.objects.create(username='testuser1', password='999555111')
#         test_user2 = User.objects.create(username='testuser2', password='111222333')
#         test_user1.save()
#         test_user2.save()
#
#     # def test_redirect_if_not_logged_in(self):
#     #     response = self.client.get(reverse('login'))
#     #     self.assertRedirects(response, '/login/')
#
#     def test_logged_in_uses_correct_template(self):
#         login = self.client.login(username='testuser1', password='999555111')
#         response = self.client.get(reverse('login'))
#
#         # Check our user is logged in
#         self.assertEqual(str(response.context['user']), 'testuser1')
#         # Check that we got a response "success"
#         self.assertEqual(response.status_code, 200)
#
#         # Check we used correct template
#         self.assertTemplateUsed(response, '/login.html')
