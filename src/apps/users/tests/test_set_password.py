from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError

from ..serializers import SetPasswordSerializer


class SetPasswordTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "Pas5w0rd"
        cls.new_password = "new_password"
        cls.user = mixer.blend("users.User")
        cls.token = PasswordResetTokenGenerator().make_token(cls.user)

    def test_validate_password_with_valid_password(self):
        """Validate password"""
        serializer = SetPasswordSerializer(
            data={"password": self.password, "user_id": self.user.pk, "token": self.token}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["password"], self.password)

    def test_validate_password_with_invalid_password(self):
        """Validate password with invalid password"""
        token = PasswordResetTokenGenerator().make_token(self.user)
        serializer = SetPasswordSerializer(data={"password": "123456", "user_id": self.user.pk, "token": self.token})
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertIn("password", str(error.exception))

    def test_validate_with_valid_token_and_user_id(self):
        """Validate valid token and user id"""
        serializer = SetPasswordSerializer(
            data={"user_id": self.user.pk, "token": self.token, "password": self.new_password}
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["token"], self.token)

    def test_validate_with_invalid_token_and_user_id(self):
        """Validate with invalid token"""
        serializer = SetPasswordSerializer(
            data={"user_id": self.user.pk, "token": "invalid_token", "password": self.new_password}
        )
        with self.assertRaises(ValidationError) as error:
            serializer.is_valid(raise_exception=True)
        self.assertIn("The token is not valid", str(error.exception))

    def test_save(self):
        """Test set password"""
        serializer = SetPasswordSerializer(
            data={"user_id": self.user.pk, "token": self.token, "password": self.new_password}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(validated_data=serializer.validated_data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))
