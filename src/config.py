# flask application configuration file

DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESSION_KEY = "csrf_secret_key"

SECRET_KEY = "app_secret_key"

