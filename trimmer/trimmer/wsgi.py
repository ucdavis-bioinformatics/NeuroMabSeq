"""
WSGI config for trimmer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

path = '/Users/keithmitchell/Desktop/Repositories/NeuroMabSeq/trimmer'
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trimmer.settings')


application = get_wsgi_application()
