Requirements
==================

! requires JSONField from Django1.9 along with PostgeSQL DB

.. code-block :: shell

    aptitude install python-virtualenv
    virtualenv .ve
    source ./ve/bin/activate
    pip install -r requirements.txt
    

Installation
=================

We are using virtualenv, django 1.8+ and pip for puling dependencies. Currently we develop on Ubuntu and we also test for this environment.

.. code-block :: shell

    virtualenv .ve
    source .ve/bin/activate
    cd deploy
    ./deploy.sh
    
tests will also require:

.. code-block :: shell

    aptitude install wamerican

JavaScript/NodeJs/Angular/Grunt:

.. code-block :: shell

    source .ve/bin/activate
    curl -sL https://deb.nodesource.com/setup | sudo bash -
    sudo apt-get install nodejs
    sudo apt-get install build-essential
    sudo npm install -g grunt-cli bower
    # inside darg.js dir:
    # where package.json file is:
    sudo npm install
    # where bowser.json is:
    bower install
    # in dir where gruntfile is to compile assets
    grunt
    
run grunt watch to autcompile assets:

.. code-block :: shell

    grunt

Dev Env
=======================

.. code-block :: shell

    pip install -r requirements_ci.txt
    ./manage.py runserver 0.0.0.0:9000 --settings=project.settings.dev

to use dev env settings for better development/debugging.

Prod Env
=====================
Using uwsgi for running on a socket.
