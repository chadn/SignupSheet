"""
Dev-Mode settings. Focus on convenience. 
"""

import secrets 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'YAJeOTGEU0gT_QlAj9ZwQF06yy46TrNUa2tdKVNC_PYIVVEpTKuJTZXiyTXBOmO2vSCy-Ck_7yL-BAAqx-8rfQ'
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'signup',
        'CLIENT': {
            'host': 'localhost',
            'username': 'root',
            'password': 'example',
        }
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
AUTH_PASSWORD_VALIDATORS = []
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CSRF_TRUSTED_ORIGINS = []
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
