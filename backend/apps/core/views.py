from apps.authentication.services import AzureADJWTService
from apps.authentication.utils import (
    extract_token_from_header,
    get_user_info_from_claims,
)
from jwt.exceptions import InvalidTokenError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    """
    Dashboard API endpoint that returns user data.
    Matches the frontend's expected UserData type.
    """
    try:
        # Get the authenticated user (set by AzureADAuthentication)
        user = request.user

        # Get the raw token to extract fresh claims
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")

        try:
            # Extract token and get claims for additional info
            token = extract_token_from_header(auth_header)
            jwt_service = AzureADJWTService()
            claims = jwt_service.validate_token(token)

            # Get user info from claims (includes welcome message)
            user_data = get_user_info_from_claims(claims)

        except (InvalidTokenError, Exception):
            # Fallback to basic user data if token re-validation fails
            user_data = {
                "username": user.username,
                "email": user.email,
                "full_name": user.get_full_name() or user.username,
                "message": "Welcome to the dashboard!",
            }

        print(f"Dashboard accessed by user: {user.username}")

        return Response(user_data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return Response(
            {"error": "Unable to load dashboard data"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
