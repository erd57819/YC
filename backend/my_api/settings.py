# backend/my_api/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv # dotenv 임포트

BASE_DIR = Path(__file__).resolve().parent.parent

# .env 파일 로드 (BASE_DIR에 .env 파일이 있다고 가정)
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=dotenv_path)

# SECRET_KEY, DEBUG 등도 .env에서 가져오도록 수정
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your_default_secret_key_if_env_is_missing')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True' # 문자열 'True'와 비교

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'articles',
    'accounts',
    'financials', #
    'golds', #
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'corsheaders', #
    'django.contrib.sites', #
    'allauth', #
    'allauth.account', #
    'allauth.socialaccount', #
    'dj_rest_auth.registration', #
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SITE_ID = 1 #

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # 기본적으로 모든 접근 허용 (필요시 수정)
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', #
]

CORS_ALLOWED_ORIGINS = [ #
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]

ROOT_URLCONF = 'my_api.urls' #

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

WSGI_APPLICATION = 'my_api.wsgi.application' #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'ko-kr' # 한국어로 변경 권장
TIME_ZONE = 'Asia/Seoul' # 시간대 변경 권장
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User' #

REST_AUTH = { #
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserProfileSerializer',
}

# --- API 키 설정 ---
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
FSS_API_KEY = os.environ.get('FSS_API_KEY')

if not OPENAI_API_KEY:
    print("★★★★★ 중요 경고: OPENAI_API_KEY가 .env에서 로드되지 않았거나 설정되지 않았습니다. AI 추천 기능이 작동하지 않습니다. ★★★★★")
if not FSS_API_KEY:
    print("경고: FSS_API_KEY가 .env에서 로드되지 않았거나 설정되지 않았습니다. 금융 상품 정보 로딩에 문제가 있을 수 있습니다.")
# 