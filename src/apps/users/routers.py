from rest_framework.routers import SimpleRouter

from .views import AuthViewSet, PasswordViewSet, UserViewSet

PUBLIC_USER_ROUTER = SimpleRouter()

PUBLIC_USER_ROUTER.register("auth", AuthViewSet, basename="auth")
PUBLIC_USER_ROUTER.register("password", PasswordViewSet, basename="password")
PUBLIC_USER_ROUTER.register("users", UserViewSet, basename="users")
