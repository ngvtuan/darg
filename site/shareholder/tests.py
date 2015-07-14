import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from shareholder.models import *
from shareholder.generators import ShareholderGenerator, PositionGenerator, UserGenerator

class CoutnryTestCase(TestCase):

    def test_model(self):

        Country.objects.create(iso_code='de_De', name="Germany")

        qs = Country.objects.all()
        country = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(country.iso_code, 'de_De')
        self.assertEqual(country.name, 'Germany')


class UserProfileTestCase(TestCase):

    def test_model(self):

        user=UserGenerator().generate()

        qs = UserProfile.objects.all()
        profile = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(profile.country.iso_code, 'de')
        self.assertEqual(profile.country.name, 'Germany') 
        self.assertEqual(profile.province, 'Some Province')

class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)

    def test_shareholder_detail(self):
        """ test detail view for shareholder """

        shareholder = ShareholderGenerator().generate()

        response = self.client.login(username=shareholder.user.username, password="test")
        self.assertTrue(response)

        response = self.client.get(reverse("shareholder", args=(shareholder.id,)))

        self.assertTrue(shareholder.user.userprofile.company_name in response.content)
        self.assertTrue(shareholder.user.userprofile.street in response.content)
        

    def test_share_percent(self):
        shareholder = ShareholderGenerator().generate()
        positions = PositionGenerator().generate(shareholder=shareholder)

        res = shareholder.share_percent()

        self.assertEqual(res, 100.0)
