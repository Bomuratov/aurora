from .settings import *
import os
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "koyebdb",
        "USER": "aurora",
        "PASSWORD": "npg_QGriLCUpA58c",
        "HOST": "ep-empty-term-a22mzt2a.eu-central-1.pg.koyeb.app",
        "PORT": "5432",
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "aurora",
#         "USER": "aurora",
#         "PASSWORD": "admin",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

