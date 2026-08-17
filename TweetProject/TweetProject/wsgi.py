"""
WSGI config for TweetProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set correct settings module based on environment
if os.getenv("DEBUG") == "False" or os.getenv("RENDER") or os.getenv("VERCEL"):
    # Production environment
    os.environ["DJANGO_SETTINGS_MODULE"] = "TweetProject.TweetProject.production_settings"
else:
    # Development environment
    os.environ["DJANGO_SETTINGS_MODULE"] = "TweetProject.TweetProject.settings"

application = get_wsgi_application()
