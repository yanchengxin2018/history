"""Django settings for djangoreactredux project."""

import os
import sys
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # remove /sswmain/settings to get base folder
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist
# Chinese http://python.usyiyi.cn/translate/Django_111/howto/deployment/checklist.html

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ajsdgas7&*kosdsa21[]jaksdhlka-;kmcv8l$#diepsm8&ah^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = "users.UserProfile"

TRACK_PAGEVIEWS = True

# Application definition
SITE_ID = 1
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'rest_framework',
    'knox',
    'django_extensions',

    # 'accounts',
    'base',

    'users.apps.UsersConfig',
    'courses.apps.CoursesConfig',
    'organization.apps.OrganizationConfig',
    'sketch.apps.SketchConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',

    # 'xadmin',
    'crispy_forms',
    'django_filters',
    'DjangoUeditor',
    'corsheaders',
    # 'users',

    # 'tracking',

)


MIDDLEWARE = (
    #'tracking.middleware.VisitorTrackingMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware'
)

CORS_ORIGIN_ALLOW_ALL = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ROOT_URLCONF = 'djangoreactredux.urls'

WSGI_APPLICATION = 'djangoreactredux.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
# 设置时区 http://python.usyiyi.cn/translate/Django_111/topics/i18n/index.html

LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8之前使用 zh-cn

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 默认是True, 时间是 utc，由于我们要用本地时间，所以手动修改为 False!!!
# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True

# AUTH_USER_MODEL = 'accounts.User'

# ACCOUNT_ACTIVATION_DAYS = 7  # days

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# http://python.usyiyi.cn/translate/Django_111/howto/static-files/index.html

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_dist'),
)

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# store static files locally and serve with whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ############# REST FRAMEWORK ###################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

# ############ REST KNOX ########################
REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'USER_SERIALIZER': 'knox.serializers.UserSerializer'
}

# 自定义用户验证
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

# Django rest framework JWT 设置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片网设置
APIKEY = "a071913802e5d5fa50fb619b4a865b4a"

# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.oxyak.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "customer@oxyak.com"
EMAIL_HOST_PASSWORD = "Root123456"
# EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_FROM = "customer@oxyak.com"

# 支付宝相关配置
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_key_2048.txt')
appid = "2017092808973751"
return_url = "http://www.oxyak.com/alipay/return/"
