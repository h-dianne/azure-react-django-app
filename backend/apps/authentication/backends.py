from apps.users.models import User
from django.contrib.auth.backends import BaseBackend
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .services import AzureADJWTService
from .utils import extract_token_from_header


class AzureADAuthentication(BaseAuthentication):
    """
    DRF Authentication class for Azure AD JWT tokens.
    """

    def __init__(self):
        self.jwt_service = AzureADJWTService()

    def authenticate(self, request):
        """
        Authenticate request using Azure AD JWT token.

        Args:
            request: Django request object

        Returns:
            tuple: (user, token) if authenticated, None otherwise

        Raises:
            AuthenticationFailed: If authentication fails
        """
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            return None

        try:
            # Extract token from header
            token = extract_token_from_header(auth_header)

            # Validate token and get claims
            claims = self.jwt_service.validate_token(token)

            # Get or create user from claims
            user, created = User.objects.get_or_create_from_azure_claims(claims)

            if created:
                print(f"Created new user from Azure AD: {user.username}")
            else:
                print(f"Authenticated existing user: {user.username}")

            return (user, token)

        except ExpiredSignatureError:
            print("Authentication failed: Token expired")
            raise AuthenticationFailed("Token has expired")

        except InvalidTokenError as e:
            print(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed("Invalid token")

        except PermissionError as e:
            print(f"Authentication failed: {str(e)}")
            raise AuthenticationFailed("User creation not allowed")

        except Exception as e:
            print(f"Unexpected authentication error: {str(e)}")
            raise AuthenticationFailed("Authentication failed")

    def authenticate_header(self, request):
        """
        Return WWW-Authenticate header for 401 responses.
        """
        return 'Bearer realm="Azure AD"'


class AzureADBackend(BaseBackend):
    """
    Django authentication backend for Azure AD.
    """

    def authenticate(self, request, token=None, **kwargs):
        """
        Authenticate using Azure AD token.
        """
        if not token:
            return None

        try:
            jwt_service = AzureADJWTService()
            claims = jwt_service.validate_token(token)
            user, _ = User.objects.get_or_create_from_azure_claims(claims)
            return user
        except Exception:
            return None

    def get_user(self, user_id):
        """
        Get user by ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
