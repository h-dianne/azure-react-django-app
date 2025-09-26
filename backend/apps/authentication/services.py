import base64

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings
from django.core.cache import cache
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class AzureADJWTService:
    """
    JWT validation service for Azure AD tokens.
    Implements 24-hour caching.
    """

    CACHE_KEY_JWKS = "azure_ad_jwks"
    CACHE_TIMEOUT = 86400  # 24 hours in seconds

    def __init__(self):
        self.tenant_id = settings.AZURE_AD["TENANT_ID"]
        self.client_id = settings.AZURE_AD["CLIENT_ID"]
        self.audience = settings.AZURE_AD["AUDIENCE"]
        self.issuer = settings.AZURE_AD["ISSUER"]
        self.jwks_uri = settings.AZURE_AD["JWKS_URI"]

    def validate_token(self, token):
        """
        Validate JWT token and return claims.

        Args:
            token (str): JWT token from Authorization header

        Returns:
            dict: Token claims if valid

        Raises:
            InvalidTokenError: If token is invalid
            ExpiredSignatureError: If token is expired
        """
        try:
            # Get public keys for validation
            public_keys = self._get_public_keys()

            # Decode token header to get key ID
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            if not kid:
                raise InvalidTokenError("Token missing key ID")

            # Find matching public key
            public_key = self._find_public_key(public_keys, kid)
            if not public_key:
                raise InvalidTokenError("Public key not found")

            # Validate and decode token
            claims = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": True,
                    "verify_iss": True,
                },
            )

            print(f"Successfully validated token for user: {claims.get('oid')}")
            return claims

        except ExpiredSignatureError:
            print("Token has expired")
            raise
        except InvalidTokenError as e:
            print(f"Invalid token: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error validating token: {str(e)}")
            raise InvalidTokenError("Token validation failed")

    def _get_public_keys(self):
        """
        Get Azure AD public keys with 24-hour caching.

        Returns:
            dict: JWKS public keys
        """
        # Try to get from cache first
        public_keys = cache.get(self.CACHE_KEY_JWKS)

        if public_keys is None:
            print("Fetching Azure AD public keys from JWKS endpoint")
            public_keys = self._fetch_public_keys()

            # Cache for 24 hours
            cache.set(self.CACHE_KEY_JWKS, public_keys, self.CACHE_TIMEOUT)
            print("Cached Azure AD public keys for 24 hours")
        else:
            print("Using cached Azure AD public keys")

        return public_keys

    def _fetch_public_keys(self):
        """
        Fetch public keys from Azure AD JWKS endpoint.

        Returns:
            dict: JWKS response

        Raises:
            requests.RequestException: If request fails
        """
        try:
            response = requests.get(
                self.jwks_uri,
                timeout=10,  # 10 second timeout
                headers={"User-Agent": "django-azure-ad-jwt/1.0"},
            )
            response.raise_for_status()

            jwks = response.json()
            print(f"Successfully fetched {len(jwks.get('keys', []))} public keys")
            return jwks

        except requests.RequestException as e:
            print(f"Failed to fetch public keys: {str(e)}")
            raise InvalidTokenError("Unable to fetch public keys")

    def _find_public_key(self, jwks, kid):
        """
        Find public key by key ID.

        Args:
            jwks (dict): JWKS response
            kid (str): Key ID from token header

        Returns:
            str: RSA public key in PEM format or None
        """
        keys = jwks.get("keys", [])

        for key in keys:
            if key.get("kid") == kid:
                return self._convert_jwk_to_pem(key)

        print(f"Public key not found for kid: {kid}")
        return None

    def _convert_jwk_to_pem(self, jwk):
        """
        Convert JWK to PEM format for PyJWT.

        Args:
            jwk (dict): JSON Web Key

        Returns:
            str: RSA public key in PEM format
        """
        try:
            # Extract modulus and exponent
            n = int.from_bytes(
                base64.urlsafe_b64decode(jwk["n"] + "=="), byteorder="big"
            )
            e = int.from_bytes(
                base64.urlsafe_b64decode(jwk["e"] + "=="), byteorder="big"
            )

            # Create RSA public key
            public_key = rsa.RSAPublicNumbers(e, n).public_key()

            # Convert to PEM format
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

            return pem.decode("utf-8")

        except Exception as e:
            print(f"Failed to convert JWK to PEM: {str(e)}")
            raise InvalidTokenError("Invalid public key format")
