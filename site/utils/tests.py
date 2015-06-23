from django.test import TestCase

from utils.user import make_username

class UtilsTestCase(TestCase):

    def test_make_username(self):

        first_name = 'Hans Walter Peter Joao'
        last_name = 'Andreesen-Horowitz Meisen Steuer'
        email = 'thisisaverylongandnonrelevant@emailaddressforsomecompany.com'

        username = make_username(first_name, last_name, email)

        self.assertTrue(len(username) > 0)
        self.assertTrue(len(username) < 30)
        self.assertTrue(isinstance(username, str))
