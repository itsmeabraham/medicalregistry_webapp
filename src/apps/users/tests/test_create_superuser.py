from django.test import TestCase

from ..models import User


class UserTest(TestCase):
    def test_create_superuser(self):
        """Create Super User"""
        user = User.objects.create_superuser("super@mail.com", "Pas5w0rd")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user(self):
        """Create User"""
        user = User.objects.create_user("user@mail.com", "Pas5w0rd")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_without_password(self):
        """Create User Without password"""
        user = User.objects.create_user_without_password("user@mail.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.password, "")
