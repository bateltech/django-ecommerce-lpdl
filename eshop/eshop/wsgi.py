"""
WSGI config for eshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Add the directory containing your Django project to the Python path
sys.path.append("C:\\Users\\Aser\\Desktop\\pierre_de_lune\\eshop")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshop.settings')

application = get_wsgi_application()
