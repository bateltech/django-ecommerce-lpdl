"""
WSGI config for eshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from dotenv import load_dotenv

# Add the directory containing your Django project to the Python path
# sys.path.append("C:\\Users\\Aser\\Desktop\\pierre_de_lune\\eshop")
sys.path.append("/home/sysadmin/lapierredelune/django-ecommerce-lpdl/eshop")

# Determine the path to the .env file
# Get the directory of the current file (wsgi.py)
current_directory = os.path.dirname(__file__)

# Move up two directory levels (the root of your project) and construct the path to the .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(current_directory)), '.env')
load_dotenv(dotenv_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshop.settings')

application = get_wsgi_application()
