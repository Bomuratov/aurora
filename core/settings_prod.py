from .settings import *
from dotenv import load_dotenv
load_dotenv()
DEBUG = False

DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "aurora"),
        "USER": os.environ.get("POSTGRES_USER", "aurora"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "admin"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
   }
}

#DATABASES = {
#   "default": {
#       "ENGINE": "django.db.backends.postgresql",
#       "NAME": "aurora",
#       "USER": "aurora",
#       "PASSWORD": "N4:>g0z}r2Xx",
#       "HOST": "localhost",
#       "PORT": "5432",
#   }
#}
