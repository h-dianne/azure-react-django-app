from jwt.exceptions import InvalidTokenError


def extract_token_from_header(auth_header):
    """
    Extract JWT token from Authorization header.

    Args:
        auth_header (str): Authorization header value

    Returns:
        str: JWT token

    Raises:
        InvalidTokenError: If header format is invalid
    """
    if not auth_header:
        raise InvalidTokenError("Authorization header missing")

    parts = auth_header.split()

    if len(parts) != 2:
        raise InvalidTokenError("Invalid authorization header format")

    scheme, token = parts

    if scheme.lower() != "bearer":
        raise InvalidTokenError("Authorization scheme must be Bearer")

    if not token:
        raise InvalidTokenError("Token missing")

    return token


def get_user_info_from_claims(claims):
    """
    Extract user information from JWT claims with sensible fallbacks.

    Tries (in order):
    - username: preferred_username (before @) -> name's first token -> upn/email (before @)
    - email: email -> upn -> preferred_username if it looks like an email
    - full_name: given_name + family_name -> name
    """
    preferred = claims.get("preferred_username") or claims.get("upn") or ""
    given = claims.get("given_name", "")
    family = claims.get("family_name", "")
    name = claims.get("name", "")

    # Email: explicit email -> upn -> preferred_username if it contains '@'
    email = claims.get("email") or claims.get("upn")
    if not email and "@" in preferred:
        email = preferred

    # Username derivation
    if preferred:
        username = preferred.split("@")[0]
    elif email:
        username = email.split("@")[0]
    elif name:
        username = name.split()[0] if name else ""
    else:
        username = ""

    # Full name derivation
    full_name = f"{given} {family}".strip() or name

    return {
        "username": username,
        "email": email,
        "full_name": full_name,
        "message": "Welcome back! Last login from Azure AD.",
    }
