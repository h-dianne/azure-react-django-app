from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class AzureUserManager(UserManager):
    """Custom user manager for Azure AD integration."""

    def get_or_create_from_azure_claims(self, claims):
        """
        Get or create user from Azure AD claims based on USER_CREATION_POLICY.
        """
        azure_oid = claims.get("oid")
        if not azure_oid:
            raise ValueError("Azure OID not found in claims")

        # Try to find existing user by azure_oid
        try:
            return self.get(azure_oid=azure_oid), False
        except self.model.DoesNotExist:
            pass

        # Handle user creation based on policy
        policy = getattr(settings, "USER_CREATION_POLICY", "auto_create")

        if policy == "auto_create":
            return self._create_user_from_claims(claims), True
        else:
            raise PermissionError("User creation not allowed")

    def _create_user_from_claims(self, claims):
        """Create new user from Azure AD claims."""
        user_data = {
            "azure_oid": claims.get("oid"),
            "username": claims.get("preferred_username")
            or claims.get("upn")
            or claims.get("email"),
            "email": claims.get("email") or claims.get("upn"),
            "first_name": claims.get("given_name", ""),
            "last_name": claims.get("family_name", ""),
        }

        # Clean up username (remove domain if email-like)
        if user_data["username"] and "@" in user_data["username"]:
            user_data["username"] = user_data["username"].split("@")[0]

        return self.create_user(**user_data)


class User(AbstractUser):
    """
    Custom User model with Azure AD integration.
    Extends Django's AbstractUser to add Azure AD Object ID (oid).
    """

    azure_oid = models.CharField(
        max_length=36,
        unique=True,
        null=True,
        blank=True,
        help_text="Azure AD Object ID for SSO integration",
    )

    objects = AzureUserManager()

    def __str__(self):
        return self.username or self.email

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
