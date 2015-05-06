from rest_framework.test import APIClient
from rest_framework import status

from django.test import TestCase

# Create your tests here.
class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_invitee_valid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/', {"email":"kk@ll.de"}, format='json')

        self.assertEqual(response.data, {'first_name': u'', 'last_name': u'', 'email': u'kk@ll.de', 'operator_set': []})

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
