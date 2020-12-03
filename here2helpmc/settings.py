# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

import os, sys, environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import django.conf.locale
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
ENVIRONMENT = env('ENVIRONMENT')
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY')


GOOGLE_API_KEY = GOOGLE_MAPS_API_KEY

ALLOWED_HOSTS = ['127.0.0.1', 'here2helpmc.app', 'www.here2helpmc.app', ]

SITE_ID = 1


SITE_NAME = 'here2helpmc'
SITE_SUPPORT_EMAIL = env('ADMIN_EMAIL')

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #THIRD PARTY
    'impersonate',
    'sekizai',
    'stronghold',
    'crispy_forms',
    'anymail',
    'mail_templated',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'address',
    'djrichtextfield',

    # ALLAUTH SOCIAL PROVIDERS 
    'allauth.socialaccount.providers.google',    


    #APPLICATION APPS
    'users.apps.UsersConfig',
    'orders.apps.OrdersConfig',
    'shared.apps.SharedConfig',
]

# https://medium.com/@royprins/django-custom-user-model-email-authentication-d3e89d36210f
AUTH_USER_MODEL = 'users.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'


CRISPY_TEMPLATE_PACK = 'bootstrap4'

ANYMAIL = {
    "SENDINBLUE_API_KEY": env('SENDINBLUE_API_KEY'),
}
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
DEFAULT_FROM_EMAIL = SITE_SUPPORT_EMAIL
SERVER_EMAIL = SITE_SUPPORT_EMAIL



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # existing backend
    'allauth.account.auth_backends.AuthenticationBackend',
)



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'impersonate.middleware.ImpersonateMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',

]

ROOT_URLCONF = 'here2helpmc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'shared/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'shared.custom_context_processor.custom_proc',
            ],
        },
    },
]

WSGI_APPLICATION = 'here2helpmc.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'here2helpmc.db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
    # ('am', _('Amharic')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# # from https://stackoverflow.com/a/20265032/13755427
# EXTRA_LANG_INFO = {
#     'am': {
#         'bidi': False,
#         'code': 'am',
#         'name': 'Amharic',
#         'name_local': u'\u12A0\u121B\u122D\u129B', #https://www.online-toolz.com/tools/text-unicode-entities-convertor.php
#     },
# }
# # Add custom languages not provided by Django
# LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
# django.conf.locale.LANG_INFO = LANG_INFO

# # plural error fix: https://stackoverflow.com/a/61474489/13755427



TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'shared/static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder", 
]


ADMIN_URL = env('ADMIN_URL')
ADMIN_EMAIL = env('ADMIN_EMAIL')
ADMINS = (
    ('admin', ADMIN_EMAIL),
)

# DEBUG TOOLBAR
if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'shared.custom_middleware.Here2HelpMCMiddleware',
    ]

    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
        'rosetta',
    )

    #Django Debug Toolbar Configuration
    #URL:  https://github.com/django-debug-toolbar/django-debug-toolbar
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
        'INTERCEPT_REDIRECTS': False
    }



# DJANGO-IMPERSONATE
IMPERSONATE_REDIRECT_URL = '/'
IMPERSONATE_URI_EXCLUSIONS = [f'^/{ ADMIN_URL }.+$', ]
IMPERSONATE_REQUIRE_SUPERUSER = True
IMPERSONATE_ALLOW_SUPERUSER = True


# DJANGO-STRONGHOLD
STRONGHOLD_DEFAULTS = True
STRONGHOLD_PUBLIC_URLS = (
    r'^/__debug__/.+$',
    r'^/i18n/setlang/?$',
)
STRONGHOLD_PUBLIC_NAMED_URLS = (
    'account_login',
    'google_login',
    'google_callback',
    'account_signup',
    'map',
)


if not DEBUG:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        send_default_pii=True
    )


TINY_API_KEY = env('TINY_API_KEY')
DJRICHTEXTFIELD_CONFIG = {
    'js': [f'//cdn.tiny.cloud/1/{TINY_API_KEY}/tinymce/5/tinymce.min.js'],
    'init_template': 'djrichtextfield/init/tinymce.js',
    'settings': {
        'menubar': False,
        'plugins': 'link image',
        'toolbar': 'bold italic | link image | removeformat',
        'width': 700
    }
}


#APPLICATION STUFF
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('processed', 'Processed and Assigned a Driver'),
    ('ready', 'Ready for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

ORDER_WEIGHT = 2.75
GOOGLE_MAP_OF_DROPOFF_LOCATIONS = 'https://www.google.com/maps/d/edit?mid=1q6xRmhM0jnLxZDcZk-EmkFI2ZdJCpImb&usp=sharing'
MONTGOMERY_COUNTY_ZIPCODES = ['20810', '20812', '20811', '20814', '20816', '20815', '20818', '20817', '20830', '20827', '20833', '20832', '20838', '20837', '20841', '20839', '20842', '20849', '20848', '20851', '20850', '20853', '20852', '20855', '20854', '20859', '20857', '20861', '20860', '20866', '20862', '20871', '20868', '20874', '20872', '20876', '20875', '20878', '20877', '20880', '20879', '20883', '20058', '20882', '20886', '20895', '20896', '20899', '20902', '20901', '20904', '20903', '20906', '20905', '20907', '20910', '20912']