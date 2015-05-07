from django.test import TestCase
from django.test.client import Client

class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content) 
