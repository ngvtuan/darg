from django.test import TestCase
from django.test.client import Client

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

        UserProfile.objects.create(user=UserGenerator().generate(),
            province='some province', street='some street', postal_code='some postal code',
            city='some city', country=Country.objects.create(iso_code='de', name='Germ'))

        qs = UserProfile.objects.all()
        profile = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(profile.country.iso_code, 'de')
        self.assertEqual(profile.country.name, 'Germ') 
        self.assertEqual(profile.province, 'some province')

class ShareholderTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)

    def test_share_percent(self):
        shareholder = ShareholderGenerator().generate()
        positions = PositionGenerator().generate(shareholder=shareholder)

        res = shareholder.share_percent()

        self.assertEqual(res, 100.0)
