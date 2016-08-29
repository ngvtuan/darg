#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.base')

from django.conf import settings  # noqa


class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client(settings.RAVEN_CONFIG.get('dsn'))

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

app = Celery(__name__)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
