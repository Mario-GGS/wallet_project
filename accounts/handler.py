from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

def register_user_handler(*, email: str, first_name: str, last_name: str, password: str, **extrafields) -> CustomUser:
    user = CustomUser(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    user.save()
    return user

def login_user_handler(*, user:CustomUser) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }