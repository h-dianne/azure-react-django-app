from decouple import config

# Determine which settings to use based on environment
ENVIRONMENT = config("DJANGO_ENVIRONMENT", default="development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "test":
    from .test import *
else:
    from .development import *
