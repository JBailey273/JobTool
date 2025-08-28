# Fix DisallowedHost by auto-including Render's hostname and building CSRF origins.
# Overwrite config/settings.py with this complete file.

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# Core settings
# --------------------------------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-insecure-change-me')
DEBUG = os.getenv('DEBUG', '0') in {'1', 'true', 'True'}


def _env_list(key: str) -> list[str]:
    return [s.strip() for s in os.getenv(key, '').split(',') if s.strip()]

# Start with any explicit env values
ALLOWED_HOSTS = _env_list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = _env_list('CSRF_TRUSTED_ORIGINS')

# Always allow local dev
ALLOWED_HOSTS += ['localhost', '127.0.0.1']

# Include Render-provided external hostname automatically
_render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')  # e.g. jobtool-web.onrender.com
if _render_host:
    ALLOWED_HOSTS.append(_render_host)
    CSRF_TRUSTED_ORIGINS.append(f'https://{_render_host}')

# De-duplicate while preserving order
_seen = set()
ALLOWED_HOSTS = [h for h in ALLOWED_HOSTS if not (h in _seen or _seen.add(h))]
_seen.clear()
CSRF_TRUSTED_ORIGINS = [u for u in CSRF_TRUSTED_ORIGINS if not (u in _seen or _seen.add(u))]

# --------------------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
ASGI_APPLICATION = 'config.asgi.application'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# --------------------------------------------------------------------------------------
# Static files (WhiteNoise)
# --------------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# --------------------------------------------------------------------------------------
# Auth / Sessions
# --------------------------------------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --------------------------------------------------------------------------------------
# I18N
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
