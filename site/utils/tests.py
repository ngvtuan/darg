from django.test import TestCase

from utils.user import make_username

from utils.formatters import string_list_to_json


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

    def test_string_list_to_json(self):

        with self.assertRaises(ValueError):
            string_list_to_json('[]')
            string_list_to_json('1,2,3,4--10')
            string_list_to_json('1,,2,3,4-10,11-12X')

        self.assertEqual(string_list_to_json('1,2,3,4-10'), [1, 2, 3, u'4-10'])
        self.assertEqual(string_list_to_json('1,2,3,,4-10'), [1, 2, 3, u'4-10'])
