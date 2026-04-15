from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


def register_user_handler(*, email: str, full_name: str, password: str) -> CustomUser:
    user = CustomUser.objects.create_user(
        email=email,
        full_name=full_name,
        password=password
    )
    return user


def login_user_handler(*, user: CustomUser) -> dict:
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
