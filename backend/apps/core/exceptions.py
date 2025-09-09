from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler for better error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Print error for debugging (since we removed logging)
        print(f"API Error: {exc} - Status: {response.status_code}")

        # Customize the response format
        if response.status_code == 401:
            custom_response_data = {
                "error": "Authentication required",
                "detail": "Please provide a valid Azure AD token",
            }
        elif response.status_code == 403:
            custom_response_data = {
                "error": "Permission denied",
                "detail": "You do not have permission to access this resource",
            }
        elif response.status_code == 404:
            custom_response_data = {
                "error": "Not found",
                "detail": "The requested resource was not found",
            }
        else:
            # Keep original response for other errors
            return response

        return Response(custom_response_data, status=response.status_code)

    # Print unexpected errors
    print(f"Unexpected error: {exc}")
    return response
