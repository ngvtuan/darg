from django.test import TestCase
from django.test.client import Client

from django.test.client import RequestFactory

# Create your tests here.
class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)
