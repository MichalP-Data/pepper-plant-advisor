import os
import sys
from pathlib import Path

# Resolve project base directory and add to path so Django imports work
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Use the project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pepper_chat_project.settings')

from django.core.wsgi import get_wsgi_application

# Expose WSGI application for Vercel
app = get_wsgi_application()

