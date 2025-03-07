from .settings import *
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "aurora",
        "USER": "aurora",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
