from .base import *
from kombu import Exchange, Queue

DEBUG = True

MANAGERS = ADMINS

# needed to send build screenshot of FE tests
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_COOKIE_NAME = 'darg-sessionid'

TRACKING_ENABLED = True
TRACKING_CODE = 'UA-58468401-4'  # used by test

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# for local dev use this...
#NOSE_ARGS = ['--pdb', '-s', '--logging-level=WARNING']

INSTALLED_APPS = INSTALLED_APPS + ('rosetta', 'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

try:
    from .dev_local import *
except ImportError:
    pass
