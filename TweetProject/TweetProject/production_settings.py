"""
Production settings for Vercel deployment
"""

from .settings import *
import os
from decouple import config

# Override settings for production
DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Database Configuration for production
import dj_database_url

# Check for DATABASE_URL (standard) or POSTGRES_URL (Vercel Postgres)
if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600
    )
elif "POSTGRES_URL" in os.environ:
    # Vercel Postgres uses POSTGRES_URL instead of DATABASE_URL
    DATABASES["default"] = dj_database_url.config(
        default=os.environ.get("POSTGRES_URL"), conn_max_age=600
    )
else:
    # Fallback to SQLite for development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Static files (WhiteNoise)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
