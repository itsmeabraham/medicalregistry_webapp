from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .mixins import PublicMixin
from .serializers import ResetPasswordSerializer, SetPasswordSerializer, UserSerializer
from .services import send_password_reset_email


class AuthViewSet(PublicMixin, GenericViewSet):
    """
    ViewSet for Auth
    """

    def _token_action(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], serializer_class=TokenObtainPairSerializer)
    def access(self, request):
        return self._token_action(request)

    @action(detail=False, methods=["POST"], serializer_class=TokenRefreshSerializer)
    def refresh(self, request):
        return self._token_action(request)


class PasswordViewSet(PublicMixin, GenericViewSet):
    """
    ViewSet for Passwords
    """

    @action(detail=False, methods=["POST"], serializer_class=ResetPasswordSerializer)
    def reset(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        url, user = serializer.save(data)
        send_password_reset_email(user, url)

        return Response()

    @action(detail=False, methods=["POST"], serializer_class=SetPasswordSerializer)
    def confirm(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data)

        return Response()


class UserViewSet(GenericViewSet):
    """
    ViewSet for User
    """

    serializer_class = UserSerializer

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def whoami(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
