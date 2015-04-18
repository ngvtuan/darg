from .base import *
from kombu import Exchange, Queue

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MANAGERS = ADMINS

# needed to send build screenshot of FE tests
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_COOKIE_NAME = 'vbnet-sessionid'

TRACKING_ENABLED = False

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# for local dev use this...
#NOSE_ARGS = ['--pdb', '-s', '--logging-level=WARNING']

INSTALLED_APPS = INSTALLED_APPS + ('rosetta',) # 'django_nose',)
