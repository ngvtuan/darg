DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'darg',
        'USER': 'darg',
        'PASSWORD': 'darg',
        'HOST': 'localhost'
    }
}
SITE_ID = 3
SECRET_KEY = 't@0=8$(m3+gcpf#a+z2&$=q+po--_&5n4#c8o%!s-5h$w)x2m3'

RAVEN_CONFIG = {
    'dsn': (
        'http://cc2e8566f011445e8ca861dfafc5bb3c:d0e872aa4c504ce4a49f6c69f9'
        '1a10d4@sentry.ttg-dresden.de/5'
    ),
    'dsn_public': (
        'http://cc2e8566f011445e8ca861dfafc5bb3c'
        '@sentry.ttg-dresden.de/5'
    ),

}

TRACKING_CODE = 'UA-58468401-4'
