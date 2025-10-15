from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
from corsheaders.defaults import default_headers

# ---------------------- LOAD ENVIRONMENT VARIABLES -----------------------
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------- SECURITY -----------------------
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-temp-key")

# Use "True" or "False" in .env → this line safely converts it
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,thechecklistco.in,www.thechecklistco.in,checklistco-backend.onrender.com"
).split(",")

# ---------------------- APPS -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',        # public site
    'clients',     # client portal
    'billing',     # invoices
    'documents',   # document vault
    'rest_framework',
    'corsheaders',
]

# ---------------------- MIDDLEWARE -----------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "checklistco.urls"

# ---------------------- TEMPLATES -----------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "checklistco.wsgi.application"


# ---------------------- DATABASE -----------------------
import dj_database_url

# If DATABASE_URL exists (Render / production), use it; otherwise fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ---------------------- PASSWORD VALIDATION -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------- LANGUAGE & TIMEZONE -----------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ---------------------- STATIC & MEDIA FILES -----------------------

# ✅ Django Admin + static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # your existing folder

# ✅ For any extra local static (optional)
STATICFILES_DIRS = []

# ✅ Media uploads (for documents)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------- REST FRAMEWORK -----------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


# ---------------------- CORS -----------------------
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-Client-Token',
]
#  EMAIL CONFIGURATION
# ------------------------
import os

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.zoho.in")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------- DEFAULT PRIMARY KEY -----------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')