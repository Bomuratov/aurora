from .settings import *
import os
from dotenv import load_dotenv
load_dotenv()

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

