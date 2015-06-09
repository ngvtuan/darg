Aktienregister Restful API
=============================================

We are using the `Django Rest Framework <http://www.django-rest-framework.org/>`_ for the API. Please read there for more details.

Authentication
============================================

We are using `Token based authentication <http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication>`_. As recommended we are creating a new token for each new user by default.

Please note that for authentication the header must be sent with any request. e.g.:

.. code-block ::

    Authorization: Token 9944b09199c62bc22418ad846dd0e4bbdfc6ee4b
    
Authentication can be tested and validated as follows:

.. code-block ::

    curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
    
To obtain the toke a dedicated view view will return a JSON response when valid username and password fields are POSTed to the view using form data or JSON:

.. code-block :: json

    { "token" : "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }

The view is under ``services/rest/api-token-auth/`` and requires a ``POST`` with username and password attributes.


Shareholder list and details
============================================
