from django.test import TestCase
from django.urls import reverse

from accounts.models import LoginDetails, RoleMaster


class ForgotPasswordTests(TestCase):
    def setUp(self):
        role = RoleMaster.objects.create(role_name='student')
        self.user = LoginDetails.objects.create(username='student1', password='oldpass', role=role)

    def test_password_can_be_changed_from_login_page(self):
        response = self.client.post(reverse('accounts:login'), {
            'form_type': 'forgot_password',
            'username': 'student1',
            'old_password': 'oldpass',
            'new_password': 'newpass123',
            'confirm_new_password': 'newpass123',
        })

        self.user.refresh_from_db()
        self.assertEqual(self.user.password, 'newpass123')
        self.assertContains(response, 'Password changed successfully')
