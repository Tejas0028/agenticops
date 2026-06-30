from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


User = get_user_model()


class UserRegistrationService:
    """
    Handles all business logic related to user registration.
    """
    

    @staticmethod
    @transaction.atomic
    def register_user(
        *,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
    ) -> User:
        """
        Register a new user
        
        Args:
            email: User email address.
            first_name: User first name.
            last_name: User last name.
            password: Plain text password.

        Returns:
            User: Newly created user instance.
        """

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        return user
    

class AuthenticationService:
    """
    Handles user authentication and JWT token generation.
    """
    @staticmethod
    def login(
        *,
        email: str,
        password: str,
    ) -> dict:
        
        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                {
                    "detail": "Invalid email or password."
                }
            )
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(access),
        }

