import os
import datetime
#STATIC

# ROOT_URL='http://172.16.10.132:8000'
# ROOT_URL='http://118.25.213.122:8889'

#部署的时候填写真实ip
# CODE_URL='118.25.213.122:8889'

# CODE_URL='127.0.0.1:8889'
# ROOT_URL='http://127.0.0.1:8889'

CODE_URL='118.25.213.122:8889'
ROOT_URL='http://118.25.213.122:8889'

# CODE_TEST=True
CODE_TEST=False
# CODE_USER='QT-yybb'        #短信模块的用户名
# CODE_PASSWORD='Net263yy'   #短信模块的密码
CODE_USER='QCD-whcb'         #短信模块的用户名
CODE_PASSWORD='Net263@xx'    #短信模块的密码

AUTH_USER_MODEL = "Questionnaire.Users"

# 指定可以跨域访问当前服务器(127.0.0.1:8000)的白名单
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT=os.path.join(BASE_DIR, 'static')
# STATIC_URL = 'static/'
# STATICFILES_DIRS=(BASE_DIR,'static')



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'static2'),
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@zki=kra+5m&co^y(li(ki@^39gf7j$n@cqoxsw4$0v!37vbwv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    #默认
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #依赖
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'django_filters',
    'corsheaders',

    #应用
    'Questionnaire',
    'Tools',
    'UserInfos',
    'back',
    'role',
    'newneed',
]


MIDDLEWARE = [
    #'Tools.middleware.CORSMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #cors通过
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Site.urls'

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

WSGI_APPLICATION = 'Site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

LANGUAGE_CODE = 'zh-hans'  # 'en-us'

TIME_ZONE = 'Asia/Shanghai'  # 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS=(BASE_DIR,'static')
# AUTH_USER_MODEL = 'UserInfos.Users'

#*********************REST_FRAMEWORK**************************
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'UserInfos.authentication.QuestionnaireAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
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
#*********************其他**************************

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
#短信验证码在此时间内禁止重新请求
RE_CODE_TIME=datetime.timedelta(minutes=0,seconds=5)
#短信验证码的有效时间
EFFECTIVE_TIME=datetime.timedelta(minutes=50)
#临时
CESHI='pbkdf2_sha256$120000$QUPNNow0RDCz$J0KDeq48tA5f4T9V7PAY9AjqindIeMQCGXhi7CXXgFw='
#*********************LOG**************************
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


#*********************调查问卷**************************
BIGHEAD='省负责人'
CITYHEAD='市负责人'
SCHOOLHEAD='校长'
GRADEHEAD='年级主任'
CLASSHEAD='老师'
BEATCHTEACHERSMS='您已成功注册瓦力工厂网站，您的用户名为{}，初始密码为{}，请您登陆{}，修改您的登陆密码。'

