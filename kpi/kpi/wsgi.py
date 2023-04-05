"""
WSGI config for kpi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import sys
sys.path.append('/code/kpi')

from django.core.wsgi import get_wsgi_application
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kpi.settings')
application = get_wsgi_application()

