from .base import *
import os
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    if var_name not in os.environ:
        raise ImproperlyConfigured("Set %s environment variable" % var_name)
    return os.environ[var_name]

DEBUG = True

MANAGERS = ADMINS

SESSION_COOKIE_NAME = 'darg-sessionid'

TRACKING_ENABLED = True
TRACKING_CODE = 'UA-58468401-4'  # used by test

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# for local dev use this...
# NOSE_ARGS = ['--pdb', '-s', '--logging-level=WARNING']
NOSE_ARGS = ['--nologcapture', '--with-enhanced-descriptions']

INSTALLED_APPS = INSTALLED_APPS + ('rosetta', 'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# -- SENDFILE for downloads
SENDFILE_BACKEND = 'sendfile.backends.development'

INSTAPAGE_TOKEN = get_env_variable('INSTAPAGE_TOKEN')
INSTAPAGE_ACCESS_TOKEN = get_env_variable('INSTAPAGE_ACCESS_TOKEN')
INSTPAGE_ENABLED = True

CELERY_ALWAYS_EAGER = True

try:
    from .dev_local import *
except ImportError:
    pass
