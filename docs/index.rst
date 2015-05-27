Requirements
==================

..code-block::

    pip install -r requirements.txt
    

Installation
=================

We are using virtualenv, django 1.8+ and pip for puling dependencies. Currently we develop on Ubuntu and we also test for this environment.

..code-block::

    virtualenv .ve
    source .ve/bin/activate
    cd deploy
    ./deploy.sh

Dev Env
=======================

..code-block::

    ./manage.py runserver 0.0.0.0:9000 --settings=project.settings.dev

to use dev env settings for better development/debugging.

Prod Env
=====================
Using uwsgi for running on a socket.
