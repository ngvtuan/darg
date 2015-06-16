from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from rest_framework.test import APIClient
from rest_framework import status

from shareholder.generators import UserGenerator, OperatorGenerator

def _add_company_to_user_via_rest(user):

    client = APIClient()
    response = client.post('/services/rest/api-token-auth/',
            {'username': user.username, 'password': 'test'},
            format='json'
        )
    token = user.auth_token
    
    response = client.post(
        reverse('add_company') ,{
            'name':'company',
            'count':1,
            'face_value':2
        },
        **{
            'HTTP_AUTHORIZATION': 'Token {}'.format(token.key), 
            'format': 'json', 
        }
    )

    if response.status_code in [200,201]:
        return True
    
    return False

class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content) 

    def test_start_authorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(username=user.username, password='test')
        
        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content) # tracking code here
        self.assertTrue("Willkommen" in response.content) # has welcome 
        self.assertFalse("shareholder_list" in response.content) # but has not shareholder list yet

    def test_start_authorized_with_operator(self):

        user = UserGenerator().generate()

        is_operator_added =_add_company_to_user_via_rest(user)
        self.assertTrue (is_operator_added)

        is_loggedin = self.client.login(username=user.username, password='test')

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content) # tracking code here
        self.assertTrue("Willkommen" in response.content) # has welcome
        self.assertTrue("manages companies" in response.content) # has shareholder list yet, but not shown by angular

    def test_start_nonauthorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(username=user.username, password='invalid_pw')

        self.assertFalse(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.content) # redirect to login
