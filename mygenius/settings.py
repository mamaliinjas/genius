from pathlib import Path
import os
import environ




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DJANGO_ENV = env('DJANGO_ENV', default='development')


SECRET_KEY =env('SECRET_KEY')


DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['ra-dif.com', 'www.ra-dif.com'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'django.contrib.sites',       
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'drf_yasg',
]

SITE_ID=1


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend', 
    'django.contrib.auth.backends.ModelBackend', 
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'myapp.middlewares.NoCacheMiddleware',
]

ROOT_URLCONF = 'mygenius.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR , 'template'],
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

WSGI_APPLICATION = 'mygenius.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Media Files
if os.environ.get('DJANGO_ENV') == 'production':
    MEDIA_ROOT = '/srv/mygenius/genius/media'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

# Static Files
if os.environ.get('DJANGO_ENV') == 'production':
    STATIC_ROOT = '/srv/mygenius/genius/staticfiles'
else:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/' 

# Optional: Define the directory for static files
# settings.py

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Points to the 'static' folder inside your project directory
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)


SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = env('SPOTIPY_REDIRECT_URI')
