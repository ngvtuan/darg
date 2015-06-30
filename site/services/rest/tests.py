from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

from shareholder.generators import OperatorGenerator, UserGenerator

# Create your tests here.
class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_invitee_valid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/', {"email":"kk@ll.de"}, format='json')

        self.assertEqual(response.data, {'email': u'kk@ll.de'})

    def test_invitee_invalid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/', {"email":"kk.de"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invitee_invalid_put_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.put('/services/rest/invitee/', {"email":"kk.de"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invitee_invalid_delete_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.delete('/services/rest/invitee/', {"email":"kk.de"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticate(self):
        """ authenticate, get token, and call for shareholder details """

        # prepare test data
        operator = OperatorGenerator().generate()
        user = operator.user
        user.set_password('test')
        user.save()

        # authenticate
        response = self.client.post('/services/rest/api-token-auth/', 
            {'username': user.username, 'password': 'test'},
            format='json'
        )

        self.assertEqual(response.data.get('token'), user.auth_token.key)

        # get shareholder details
        token = user.auth_token
        response = self.client.get('/services/rest/shareholders', **{'HTTP_AUTHORIZATION': 'Token {}'.format(token.key), 'format': 'json'})

        self.assertEqual(response.data.get('results'), [])

    def test_add_shareholder_for_existing_user_account(self):
        """ 
        test to add a shareholder for an existing user account. means shareholder
        was added for another or same company already. means we don't add another user object 
        """

        operator = OperatorGenerator().generate()
        user= operator.user

        logged_in = self.client.login(username=user.username, password='test')
        self.assertTrue(logged_in)

        data = {"user":
                    {
                    "first_name":"Mike",
                    "last_name":"Hildebrand",
                    "email":"mike.hildebrand@darg.com",
                    "userprofile": 
                        {
                        "company_name": "TestCorp",
                        "street": "somestreet",
                        "postal_code": "1252",
                        "province": "walter",
                        "city": "some city",
                        "country": {"iso_code": "de", "name": "Germany"},
                        "birthday": "2002-12-01",
                        }
                    },
                "number":"1000"}


        response = self.client.post('/services/rest/shareholders', data, 
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(user.auth_token.key), 'format': 'json'})

        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'1000')
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)
