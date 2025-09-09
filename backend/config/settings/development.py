from .base import *

# Debug toolbar for development
# if DEBUG:
#     INSTALLED_APPS += ["debug_toolbar"]
#     MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

#     # Debug toolbar configuration
#     INTERNAL_IPS = [
#         "127.0.0.1",
#         "localhost",
#     ]

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "azure_django_dev",
    "TIMEOUT": 300,
}

# More permissive CORS for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development (console)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Cache timeout override for development (shorter for testing)
CACHES["default"]["TIMEOUT"] = 300  # 5 minutes for development

# Allow any host in development (be careful!)
ALLOWED_HOSTS = ["*"]

# Development database (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
