# coding=utf-8
from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

User = get_user_model()

from shareholder.generators import (
    OperatorGenerator, UserGenerator, CompanyGenerator,
    ShareholderGenerator, TwoInitialSecuritiesGenerator
)
from shareholder.models import Operator, Shareholder, Position


class OperatorTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.site = Site.objects.get_current()

    def test_add_operator(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {'email': user2.email}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(user2.operator_set.filter(company=company).exists())

    def test_add_operator_wrong_email(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {"email": "a@a.de"}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertTrue('email' in response.content)

    def test_add_operator_foreign_company(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = CompanyGenerator().generate()
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {'email': user2.email}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertTrue('company' in response.content)

    def test_delete_operator(self):
        operator = OperatorGenerator().generate()
        operator2 = OperatorGenerator().generate(company=operator.company)
        user = operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            u"operator.id": operator2.id}

        response = self.client.delete(
            '/services/rest/operators/{}'.format(operator2.pk),
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Operator.objects.filter(pk=operator2.pk).exists())


class PositionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_add_position(self):
        """ test that we can add a position """

        operator = OperatorGenerator().generate()
        user = operator.user

        buyer = ShareholderGenerator().generate(company=operator.company)
        seller = ShareholderGenerator().generate(company=operator.company)
        TwoInitialSecuritiesGenerator().generate(company=operator.company)

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "bought_at": "2016-01-01T00:00:00.000Z",
            "buyer": {
                "pk": buyer.pk,
                "user": {
                    "first_name": buyer.user.first_name,
                    "last_name": buyer.user.last_name,
                    "email": buyer.user.email,
                    "operator_set": [],
                    "userprofile": None,
                },
                "number": "0",
                "company": {
                    "pk": operator.company.pk,
                    "name": operator.company.name,
                    "share_count": operator.company.share_count,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/"
                           "company/{}".format(operator.company.pk),
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "security": {
                "pk": 2,
                "readable_title": "Preferred Stock",
                "title": "P"
            },
            "count": 1,
            "value": 1,
            "seller": {
                "pk": seller.pk,
                "user": {
                    "first_name": seller.user.first_name,
                    "last_name": seller.user.last_name,
                    "email": seller.user.email,
                    "operator_set": [],
                    "userprofile": None
                },
                "number": "0",
                "company": {
                    "pk": 5,
                    "name": "LieblingzWaldCompany AG",
                    "share_count": 100100,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/company/5",
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "comment": "sdfg"
        }

        response = self.client.post(
            '/services/rest/position',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue('sdfg' in response.content)

        position = Position.objects.latest('id')
        self.assertEqual(position.count, 1)
        self.assertEqual(position.value, 1)
        self.assertEqual(position.buyer, buyer)
        self.assertEqual(position.seller, seller)


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

    def test_edit_shareholder(self):
        """ test editing shareholder data
            required for editing:
            first_name, last_name
            email
            shareholder company name
            shareholder address (street, zip, city, province, country)
            birthday
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        shareholder = ShareholderGenerator().generate(company=company)

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {
            "pk": 8,
            "user": {
                "first_name": "Mutter1Editable",
                "last_name": "KutterEditable",
                "email": "mutter@demo.ch",
                "operator_set": [],
                "userprofile": {
                    "street": "SomeStreet",
                    "city": "Hamm",
                    "province": "SomeProvince",
                    "postal_code": "932029",
                    "country": "http://codingmachine:9000/services/rest/"
                                "country/de",
                    "birthday": "2016-01-27",
                    "company_name": "SomeCompany"
                },
            },
            "number": "00333e",
            "company": {
                "pk": 5,
                "name": "LieblingzWaldCompany AG",
                "share_count": 100100,
                "country": "http://codingmachine:9000/services/rest"
                           "/country/DL",
                "url": "http://codingmachine:9000/services/rest/company/5",
                "shareholder_count": 2
            },
            "share_percent": "0.00",
            "share_count": 0,
            "share_value": 0,
            "validate_gafi": {
                "is_valid": True,
                "errors": []
            }
        }

        response = self.client.put(
            '/services/rest/shareholders/{}'.format(shareholder.pk),
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        s = Shareholder.objects.get(id=shareholder.id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get('number'), "00333e")
        self.assertEqual(s.user.first_name, "Mutter1Editable")

        userprofile = s.user.userprofile
        for k, v in data['user']['userprofile'].iteritems():
            if k == 'country':
                self.assertEqual(getattr(userprofile, k).pk, v[-2:])
                continue
            if k == 'birthday':
                self.assertEqual(
                    getattr(userprofile, k).strftime('%Y-%m-%d'), v)
                continue
            self.assertEqual(getattr(userprofile, k), v)

        # check proper db status
        user = s.user
        self.assertEqual(user.email, "mutter@demo.ch")
