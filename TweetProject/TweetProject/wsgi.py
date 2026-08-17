"""
WSGI config for TweetProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings on production, development settings locally
if os.getenv("VERCEL") or os.getenv("RENDER"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TweetProject.TweetProject.production_settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TweetProject.TweetProject.settings")

application = get_wsgi_application()
