DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'darg',                      
        'USER': 'darg',
        'PASSWORD': 'RasenSprenger775',
        'HOST': ''
    }
}
SITE_ID = 1
SECRET_KEY = 'w8_l!pca@jlk31c63zkn*+i39x5x$s5w-xw2q$#nse-38tl41('

#DEBUG = True

RAVEN_CONFIG = {
    'dsn': 'http://cc2e8566f011445e8ca861dfafc5bb3c:d0e872aa4c504ce4a49f6c69f91a10d4@aggregator.ttg-dresden.de:9000/5',
}

TRACKING_CODE = 'UA-58468401-3'
