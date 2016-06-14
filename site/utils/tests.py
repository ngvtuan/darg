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

    def test_unique_username(self):
        """
        on prod we had
        http://sentry.ttg-dresden.de/sentry-internal/production/
        issues/28313/
        jirka2@tschitschereengreen.com
        vs
        jirka+test2@kkd-partners.com
        """
        username1 = make_username(
            'Jirka', 'Schaefer', u'jirka@tschitschereengreen.com')

        username2 = make_username(
            'Jirka2', 'Schaefer2', u'jirka2@tschitschereengreen.com')

        self.assertNotEqual(username1, username2)
