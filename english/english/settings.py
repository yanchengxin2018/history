import os,datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#-----------------------------------常用-------------------------------------常用
DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS=(BASE_DIR,'static')
LANGUAGE_CODE = 'zh-hans'  # 'en-us'
TIME_ZONE = 'Asia/Shanghai'  # 'UTC'
AUTH_USER_MODEL = 'Main.UserModel'
#-----------------------------------自定义的----------------------------------自定义
IP='0.0.0.0:8000'
CODE_TEST=True
CODE_USER='QT-yybb'        #短信模块的用户名(瓦力)
CODE_PASSWORD='Net263yy'   #短信模块的密码(瓦力)
# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
#短信验证码在此时间内禁止重新请求
# RE_CODE_TIME=datetime.timedelta(minutes=1,seconds=0)
RE_CODE_TIME=datetime.timedelta(minutes=0,seconds=5)      #开发模式
#短信验证码的有效时间
EFFECTIVE_TIME=datetime.timedelta(minutes=5)

#-----------------------------------应用--------------------------------------应用
INSTALLED_APPS = [
    # 系统
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 依赖
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'corsheaders',
]

MY_APPS=[
    'Main',
]
INSTALLED_APPS+=MY_APPS
#-----------------------------------本应用----------------------------------本应用专用
LEVEL_0=datetime.timedelta(seconds=1)
LEVEL_1=datetime.timedelta(minutes=3)
LEVEL_2=datetime.timedelta(minutes=20)
LEVEL_3=datetime.timedelta(hours=3)
LEVEL_4=datetime.timedelta(days=1)
LEVEL_5=datetime.timedelta(days=5)
LEVEL_6=datetime.timedelta(days=10)
LEVEL_7=datetime.timedelta(days=30)
LEVEL_8=datetime.timedelta(days=80)
LEVEL_9=datetime.timedelta(days=365)
#-----------------------------------中间件----------------------------------中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #cors通过
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#-----------------------------------数据库----------------------------------数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#-----------------------------------开发非同源跨域访问-----------------------开发模式跨域

# 指定可以跨域访问当前服务器(127.0.0.1:8000)的白名单# 172.16.10.132
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
    'localhost:8000',
    '172.16.10.133:8000',

)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'async',
    'process-Data',
)
# 指定在跨域访问中，后台是否支持传送cookie
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True
PAGE_CACHE_SECONDS = 1
# -----------------------------------REST_FRAMEWORK----------------------------REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'Main.authentication.Authentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',


    'PAGE_SIZE': 20,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
# -----------------------------------LOG----------------------------------------LOG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['django_rest_logger_handler'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'django_rest_logger_handler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['django_rest_logger_handler'],
            'propagate': False,
        },
        'django_rest_logger': {
            'level': 'DEBUG',
            'handlers': ['django_rest_logger_handler'],
            'propagate': False,
        },
    },
}

DEFAULT_LOGGER = 'django_rest_logger'

LOGGER_EXCEPTION = DEFAULT_LOGGER
LOGGER_ERROR = DEFAULT_LOGGER
LOGGER_WARNING = DEFAULT_LOGGER



# ---------------------------一般用不到的配置-----------------------------------
SECRET_KEY = '-8dc&e!0-%5nwjgc#pawus@gvz&2b!1t)e4jgy9n$q3#@h-8+3'
ROOT_URLCONF = 'english.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'english.wsgi.application'

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
USE_I18N = True
USE_L10N = True
# USE_TZ = True
USE_TZ = False

