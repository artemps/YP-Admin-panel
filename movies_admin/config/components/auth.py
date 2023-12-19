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

AUTH_USER_MODEL = 'movies.User'

AUTHENTICATION_BACKENDS = [
    'movies.auth.CustomBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

AUTH_API_LOGIN_URL = 'http://localhost:8070/api/v1/auth/login'
AUTH_API_USER_INFO = 'http://localhost:8070/api/v1/users/me'
