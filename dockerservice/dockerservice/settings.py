"""
Django settings for dockerservice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'skbu0@@#41n)xvctr4)inl__iu*u0kl92doo)x*rjb@f&)+$l3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_auth',
    'userside',
    'djrill',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)



ROOT_URLCONF = 'dockerservice.urls'

WSGI_APPLICATION = 'dockerservice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 32
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16

SOCIAL_AUTH_ENABLED_BACKENDS = ('google')

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

GOOGLE_OAUTH2_CLIENT_ID      = '375969103681-jq77m7n63gjsvf3ehfr4g3n6q2g0qc4n.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'KxnO4pYzZ6p31seZfU9_GcAz'

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['iiitd.ac.in']

STATIC_ROOT = os.path.join(BASE_DIR, "staticdir/")

STATIC_URL = '/static/'

STATICFILES_DIRS = ( 
    (os.path.join(PROJECT_ROOT, 'static/')),
)

TEMPLATE_DIRS = ( 
    os.path.join(PROJECT_ROOT, 'templates/'),
)

STATICFILES_FINDERS = {
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
}

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

MANDRILL_API_KEY = "IAgTw__MZIpravUNZn9n2Q"

