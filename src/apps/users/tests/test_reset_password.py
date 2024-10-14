from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError

from ..serializers import ResetPasswordSerializer


class ResetPasswordTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.token = "mocked_token"
        cls.email_not_found = "nonexisting@example.com"
        cls.user = mixer.blend("users.User")

    def test_validate_email_with_existing_user(self):
        """Validate email with existing user"""
        serializer = ResetPasswordSerializer(data={"email": self.user.email})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["email"], self.user)

    def test_validate_email_with_non_existing_user(self):
        """Validate email with ni existing"""
        serializer = ResetPasswordSerializer(data={"email": self.email_not_found})
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertIn("No existe un usuario con ese email", str(error.exception))

    @patch("django.contrib.auth.tokens.PasswordResetTokenGenerator.make_token")
    def test_save(self, mock_make_auth):
        mock_make_auth.return_value = self.token
        serializer = ResetPasswordSerializer(data={"email": self.user.email})
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        expected_result = (
            f"{settings.FRONTEND_DOMAIN}{settings.FRONTEND_RESET_PASSWORD_PATH}/{self.token}?u={self.user.pk}",
            self.user,
        )
        self.assertEqual(result, expected_result)
