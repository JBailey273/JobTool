from pathlib import Path
"context_processors": [
"django.template.context_processors.debug",
"django.template.context_processors.request",
"django.contrib.auth.context_processors.auth",
"django.contrib.messages.context_processors.messages",
],
},
}
]


# --------------------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------------------
# Uses DATABASE_URL when present (Render supplies it). Fallback to local sqlite.
DATABASES = {
"default": dj_database_url.config(
default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
conn_max_age=600,
)
}


# --------------------------------------------------------------------------------------
# Static files (served by WhiteNoise)
# --------------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}


# --------------------------------------------------------------------------------------
# Auth / Sessions
# --------------------------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# --------------------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------------------------------------------
# Logging (concise prod logs)
# --------------------------------------------------------------------------------------
LOGGING = {
"version": 1,
"disable_existing_loggers": False,
"handlers": {"console": {"class": "logging.StreamHandler"}},
"root": {"handlers": ["console"], "level": "INFO"},
}
