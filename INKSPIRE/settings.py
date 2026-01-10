from pathlib import Path
import dj_database_url
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--z#e*oh_axwvilt7b33fws2l4^*(yk1o$0k4wec1=u(_ic=w27'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    "https://inkspire.up.railway.app",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',  # opcional si usas allauth, pero no hace daño
    'whitenoise.runserver_nostatic',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'Usuarios',
    'Productos',
    'cloudinary',  # cloudinary
    'cloudinary_storage',  # cloudinary

]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 👇 AÑADIR AQUÍ
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'INKSPIRE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Productos.context_processors.categorias_globales',
            ],
        },
    },
]

WSGI_APPLICATION = 'INKSPIRE.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }

DATABASES = {
   'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

AUTH_USER_MODEL = 'Usuarios.Usuario'

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

TIME_ZONE = 'America/Mexico_City'
LANGUAGE_CODE = 'es'
USE_I18N = True  #
USE_L10N = True  #
USE_TZ = True  #

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/


# Rutas de login/logout
LOGIN_URL = 'login'

SITE_ID = 1

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_ADAPTER = 'Usuarios.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'Usuarios.social_adapters.CustomSocialAccountAdapter'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
SOCIALACCOUNT_LOGIN_ON_GET = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # recolecta todo lo estatic

# MEDIA (para ImageField)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # si BASE_DIR es Path, si es str: os.path.join(BASE_DIR, 'media')

# Templates: opcional asegurar DIRS tenga templates/
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']  # ajusta según tu BASE_DIR

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  # carpeta estática en la raíz del proyecto
]
