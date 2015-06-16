from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from shareholder.generators import UserGenerator

class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content) 

    def test_start_authorized(self):

        user = UserGenerator().generate()

        self.client.login(username=user.username, password='test')

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)
