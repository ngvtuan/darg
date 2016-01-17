# coding=utf-8
from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from shareholder.generators import (
    OperatorGenerator, UserGenerator
)
from shareholder.models import Operator


class OperatorTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_add_operator(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "user": {
                "email": user2.email
            },
            "company": "http://codingmachine:9000/services/rest/company/"
            "{}".format(company.pk)
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(user2.operator_set.filter(company=company).exists())

    def test_delete_operator(self):
        operator = OperatorGenerator().generate()
        operator2 = OperatorGenerator().generate(company=operator.company)
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        response = self.client.delete(
            '/services/rest/operators/{}'.format(operator2.pk),
            {},
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Operator.objects.filter(pk=operator2.pk).exists())

    def test_delete_operator_other_company(self):
        operator = OperatorGenerator().generate()
        operator2 = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        response = self.client.delete(
            '/services/rest/operators/{}'.format(operator2.pk),
            {},
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 403)

    def test_delete_operator_myself(self):
        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        response = self.client.delete(
            '/services/rest/operators/{}'.format(operator.pk),
            {},
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 403)


class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_invitee_valid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/',
                                    {"email": "kk@ll.de"}, format='json')

        self.assertEqual(response.data, {'email': u'kk@ll.de'})

    def test_invitee_invalid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/',
                                    {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invitee_invalid_put_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.put('/services/rest/invitee/',
                                   {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invitee_invalid_delete_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.delete('/services/rest/invitee/',
                                      {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticate(self):
        """ authenticate, get token, and call for shareholder details """

        # prepare test data
        operator = OperatorGenerator().generate()
        user = operator.user
        user.set_password('test')
        user.save()

        # authenticate
        response = self.client.post(
            '/services/rest/api-token-auth/',
            {'username': user.username, 'password': 'test'},
            format='json'
        )

        self.assertEqual(response.data.get('token'), user.auth_token.key)

        # get shareholder details
        token = user.auth_token
        response = self.client.get(
            '/services/rest/shareholders',
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
               'format': 'json'
               })

        self.assertEqual(response.data.get('results'), [])

    def test_add_new_shareholder(self):
        """ addes a new shareholder and user and checks for special chars"""

        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            u"user": {
                u"first_name": u"Mike2Grüße",
                u"last_name": u"Hildebrand2Grüße",
                u"email": u"mike.hildebrand2@darg.com",
            },
            u"number": u"10002"}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'10002')
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)

        # check proper db status
        user = User.objects.get(email="mike.hildebrand2@darg.com")

    def test_add_shareholder_for_existing_user_account(self):
        """ test to add a shareholder for an existing
        user account. means shareholder
        was added for another or same company already. means we don't
        add another user object
        """

        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "user": {
                "first_name": "Mike",
                "last_name": "Hildebrand",
                "email": "mike.hildebrand@darg.com",
            },
            "number": "1000"}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'1000')
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)

        # check proper db status
        user = User.objects.get(email="mike.hildebrand@darg.com")
