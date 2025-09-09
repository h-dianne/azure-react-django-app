# Backend - Django with Azure AD JWT Authentication

A Django REST Framework backend with Azure Active Directory JWT token authentication.

## Features

- **Azure AD JWT Validation**: Secure token verification using PyJWT
- **Automatic User Management**: User creation/identification via Azure AD Object ID (oid)
- **Public Key Caching**: 24-hour caching of Azure AD public keys for performance
- **Django REST Framework**: Modern API development with DRF
- **Custom Authentication**: DRF authentication class for seamless Azure AD integration

## Technology Stack

- **Framework**: Django 5.2+ with Django REST Framework
- **Package Manager**: UV package manager
- **JWT Library**: PyJWT for token validation
- **Cryptography**: RSA signature verification with Azure AD public keys
- **Caching**: Django Redis cache for public key storage
- **HTTP Client**: Requests library for Azure AD API calls

## Implementation Details

### Authentication Architecture

- **JWT Token Validation**: RS256 algorithm with Azure AD public keys
- **Public Key Management**: Automatic fetching and 24-hour caching
- **User Resolution**: Extract Object ID (oid) from token claims
- **Security**: Audience and issuer verification for enhanced security

### Key Components

- **`AzureADAuthentication`**: DRF authentication class handling token validation
- **`AzureADJWTService`**: Service for JWT validation and public key management
- **`AzureADBackend`**: Django authentication backend for session-based auth
- **Custom User Model**: Extended user model with Azure AD Object ID support
- **Caching Layer**: Redis/Django cache for performance optimization

## Getting Started

### Prerequisites

- Python (v3.11 or higher)
- UV package manager
- Azure AD application registration

### Installation

1. **Install UV (if not already installed):**

   ```bash
   pip install uv
   ```

2. **Install dependencies and create virtual environment:**

   ```bash
   uv sync
   ```

3. **Configure environment variables:**

   Create a `.env` file in the backend directory:

   ```properties
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here

   # Azure AD Configuration
   AZURE_AD_TENANT_ID=your-tenant-id
   AZURE_AD_CLIENT_ID=your-client-id
   AZURE_AD_AUDIENCE=api://your-client-id/access_as_user
   AZURE_AD_ISSUER=https://login.microsoftonline.com/your-tenant-id/v2.0
   AZURE_AD_JWKS_URI=https://login.microsoftonline.com/your-tenant-id/discovery/v2.0/keys
   ```

4. **Run database migrations:**

   ```bash
   uv run python manage.py migrate
   ```

5. **Start the development server:**

   ```bash
   uv run python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

## Available Commands

- **`uv run python manage.py migrate`**: Run database migrations
- **`uv run python manage.py makemigrations`**: Create new migrations
- **`uv run python manage.py createsuperuser`**: Create admin user
- **`uv run python manage.py test`**: Run test suite
- **`uv run python manage.py shell`**: Django interactive shell

## Environment Variables

| Variable             | Description                     | Example                                                           |
| -------------------- | ------------------------------- | ----------------------------------------------------------------- |
| `DEBUG`              | Django debug mode               | `True`                                                            |
| `SECRET_KEY`         | Django secret key               | `your-secret-key-here`                                            |
| `AZURE_AD_TENANT_ID` | Azure AD tenant ID              | `your-tenant-id`                                                  |
| `AZURE_AD_CLIENT_ID` | Azure AD application client ID  | `your-client-id`                                                  |
| `AZURE_AD_AUDIENCE`  | Expected audience in JWT tokens | `api://client-id/access_as_user`                                  |
| `AZURE_AD_ISSUER`    | JWT issuer URL                  | `https://login.microsoftonline.com/tenant-id/v2.0`                |
| `AZURE_AD_JWKS_URI`  | Azure AD public keys endpoint   | `https://login.microsoftonline.com/tenant-id/discovery/v2.0/keys` |

## Project Structure

```text
backend/
├── apps/                    # Django applications
│   ├── authentication/     # Azure AD authentication logic
│   │   ├── backends.py     # DRF authentication classes
│   │   ├── services.py     # JWT validation service
│   │   └── utils.py        # Helper utilities
│   ├── core/               # Core application logic
│   └── users/              # User model and management
├── config/                 # Django configuration
│   ├── settings/           # Environment-specific settings
│   │   ├── base.py        # Base settings
│   │   └── development.py  # Development settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI application
├── .env                   # Environment variables (create this)
├── manage.py              # Django management script
└── pyproject.toml         # Python dependencies (UV format)
```

## Authentication Flow

### JWT Token Validation Process

1. **Token Extraction**: Extract Bearer token from Authorization header
2. **Header Validation**: Decode token header to get Key ID (kid)
3. **Public Key Retrieval**: Fetch Azure AD public keys (with 24-hour caching)
4. **Key Matching**: Find the appropriate public key using the kid
5. **Token Validation**: Verify signature, expiration, audience, and issuer
6. **Claims Extraction**: Extract user information from token claims
7. **User Resolution**: Get or create user based on Object ID (oid)

### Security Features

- **RS256 Algorithm**: Asymmetric cryptography for secure token verification
- **Audience Validation**: Ensures tokens are intended for this application
- **Issuer Verification**: Confirms tokens come from trusted Azure AD tenant
- **Expiration Check**: Respects JWT expiration claims
- **Automatic Key Rotation**: Handles Azure AD public key changes seamlessly
- **Comprehensive Error Handling**: Proper HTTP responses for authentication failures

## Azure AD Configuration

### Required Azure AD Setup

1. **App Registration**: Create an Azure AD app registration
2. **API Permissions**: Configure necessary API scopes
3. **Expose API**: Create custom scopes for your application
4. **Authentication**: Configure token settings and redirect URIs

### Token Claims

The backend expects these claims in JWT tokens:

- **`aud`**: Audience (must match AZURE_AD_AUDIENCE)
- **`iss`**: Issuer (must match AZURE_AD_ISSUER)
- **`oid`**: Object ID (used for user identification)
- **`exp`**: Expiration time
- **`sub`**: Subject identifier

## API Endpoints

### Authentication

All API endpoints require a valid Azure AD JWT token in the Authorization header:

```text
Authorization: Bearer <your-jwt-token>
```

### Example Protected Endpoint

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.authentication.backends import AzureADAuthentication

@api_view(['GET'])
def protected_view(request):
    # Authentication is handled automatically by DRF
    user = request.user  # Authenticated Azure AD user
    return Response({'message': f'Hello, {user.username}!'})
```

## Caching

The backend implements intelligent caching for Azure AD public keys:

- **Cache Duration**: 24 hours (configurable)
- **Cache Key**: `azure_ad_jwks`
- **Fallback**: Automatic refetch if cache miss
- **Performance**: Reduces API calls to Azure AD

## Error Handling

### Authentication Errors

- **`401 Unauthorized`**: Invalid or expired token
- **`403 Forbidden`**: Valid token but insufficient permissions
- **HTTP Headers**: Proper WWW-Authenticate headers for 401 responses
