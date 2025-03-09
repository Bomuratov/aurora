from .settings import *
from dotenv import load_dotenv
load_dotenv()
DEBUG = True

DATABASES = {
   "default": {
       "ENGINE": "django.db.backends.postgresql",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "aurora"),
        "USER": os.environ.get("POSTGRES_USER", "aurora"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "admin"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
   }
}
