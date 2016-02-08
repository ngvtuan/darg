from .base import *

DEBUG = True

MANAGERS = ADMINS

SESSION_COOKIE_NAME = 'darg-sessionid'

TRACKING_ENABLED = True
TRACKING_CODE = 'UA-58468401-4'  # used by test

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# for local dev use this...
# NOSE_ARGS = ['--pdb', '-s', '--logging-level=WARNING']
REUSE_DB = True
NOSE_PROGRESSIVE_EDITOR = 'vim'

INSTALLED_APPS = INSTALLED_APPS + ('rosetta', 'django_nose',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# -- SENDFILE for downloads
SENDFILE_BACKEND = 'sendfile.backends.development'

try:
    from .dev_local import *
except ImportError:
    pass
