import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

_env = BASE_DIR / '.env'
if _env.exists():
    for _l in _env.read_text(encoding='utf-8').splitlines():
        _l = _l.strip()
        if _l and not _l.startswith('#') and '=' in _l:
            _k, _v = _l.split('=', 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))

SECRET_KEY = 'django-insecure-f)ov1wh7&4zi5=xm@sq(rla^9lr%(p&adlbvvr9cv=&3la$8w#'

VERCEL = bool(os.environ.get('VERCEL'))
DEBUG = not VERCEL

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver', '.vercel.app']
CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'escola.aplicacao.EscolaConfig',
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
ROOT_URLCONF = 'gestao.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend' / 'telas_geral'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gestao.wsgi.application'
def _banco():
    url = os.environ.get('DATABASE_URL')
    if url:
        from urllib.parse import urlparse, unquote
        u = urlparse(url)
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': u.path.lstrip('/') or 'postgres',
            'USER': unquote(u.username or ''),
            'PASSWORD': unquote(u.password or ''),
            'HOST': u.hostname,
            'PORT': u.port or 5432,
            'OPTIONS': {'sslmode': 'require'},
            'CONN_MAX_AGE': 0 if VERCEL else 60,
        }
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3' if VERCEL else BASE_DIR / 'db.sqlite3',
    }


DATABASES = {'default': _banco()}
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_USE_FINDERS = True
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
STATICFILES_DIRS = [BASE_DIR.parent / 'frontend' / 'static']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
