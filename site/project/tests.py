import time

from django.core import mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from rest_framework.test import APIClient

from project.base import BaseSeleniumTestCase
from project import page
from shareholder.generators import (
    UserGenerator, CompanyGenerator, ShareholderGenerator,
    PositionGenerator, OperatorGenerator, TwoInitialSecuritiesGenerator
    )
from shareholder.models import Security, Shareholder, UserProfile


def _add_company_to_user_via_rest(user):

    client = APIClient()
    response = client.post(
        '/services/rest/api-token-auth/',
        {'username': user.username, 'password': 'test'},
        format='json'
    )
    token = user.auth_token

    response = client.post(
        reverse('add_company'), {
            'name': 'company',
            'founded_at': '2015-01-02',
            'count': 1,
            'face_value': 2
        },
        **{
            'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
            'format': 'json',
        }
    )

    if response.status_code in [200, 201]:
        return True

    return False


class IndexTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_content(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("bootstrap.min.js" in response.content)
        self.assertTrue("xeditable.min.js" in response.content)
        self.assertTrue("xeditable.css" in response.content)
        self.assertTrue("last css in" in response.content)


class InstapageTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """
        user arriving from instapage must be imported, logged in and redirected
        """
        response = self.client.get(reverse('instapage'), follow=True)

        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            reverse('instapage') + '?submission=30122798', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(
                email='jirka@tschitschereengreen.com',
                first_name='Jirka',
                last_name='Schaefer',
                is_active=True
                ).exists())
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            response.redirect_chain[0][0], 'http://testserver/start/')
        self.assertTrue(UserProfile.objects.filter(
            user__email='jirka@tschitschereengreen.com',
            tnc_accepted=True, ip='79.168.182.174').exists())
        # FIXME
        # self.assertEqual(len(mail.outbox), 1)


class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)

    def test_start_authorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(
            username=user.username, password='test')

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)
        self.assertTrue("Willkommen" in response.content)
        self.assertTrue("shareholder_list" in response.content)
        # self.assertTrue('download/pdf' in response.content)
        # self.assertTrue('download/csv' in response.content)

    def test_start_authorized_with_operator(self):

        user = UserGenerator().generate()

        is_operator_added = _add_company_to_user_via_rest(user)
        self.assertTrue(is_operator_added)

        is_loggedin = self.client.login(
            username=user.username, password='test')

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)
        self.assertTrue("Willkommen" in response.content)
        self.assertTrue("shareholder_list" in response.content)

    def test_start_nonauthorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(
            username=user.username, password='invalid_pw')

        self.assertFalse(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.content)  # redirect to login


class DownloadTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_csv_download(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))

        # initial share creation
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=1000, value=10)
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10,
            seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(
            buyer=shareholder_list[2], count=20, value=20,
            seller=shareholder_list[0])
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=20, value=20,
            seller=shareholder_list[2])

        # run test
        response = self.client.get(
            reverse('captable_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username, password='test')
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_csv',
            kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        lines = response.content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines:
            self.assertEqual(row.count(','), 5)
        self.assertEqual(len(lines), 3)  # ensure we have the right data
        # assert company itself
        self.assertEqual(shareholder_list[0].number, lines[1].split(',')[0])
        # assert share owner
        self.assertEqual(shareholder_list[1].number, lines[2].split(',')[0])
        # assert shareholder witout position not in there
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[3].number)
        # assert shareholder which bought and sold again
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[2].number)

    def test_csv_download_with_missing_operator(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))

        # initial share creation
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=1000, value=10)
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10,
            seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(buyer=shareholder_list[2], count=20, value=20, seller=shareholder_list[0])
        PositionGenerator().generate(buyer=shareholder_list[0], count=20, value=20, seller=shareholder_list[2])

        # run test
        response = self.client.get(reverse('captable_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        is_loggedin = self.client.login(username=user.username, password='test')
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_csv', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_pdf_download_(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        # run test
        response = self.client.get(reverse('captable_pdf', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username, password='test')
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_pdf', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        self.assertTrue(response.content.startswith('%PDF-1.4\r\n'))
        self.assertTrue(response.content.endswith('EOF\r\n'))

    def test_pdf_download_with_missing_operator(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        # run test
        response = self.client.get(reverse('captable_pdf', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        is_loggedin = self.client.login(username=user.username, password='test')
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_pdf', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)


# --- FUNCTIONAL TESTS
class StartFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def tearDown(self):
        Security.objects.all().delete()

    def test_ticket_49(self):
        """ add shareholder as ops and then try login as this shareholder """
        self.operator = OperatorGenerator().generate(
            user=self.buyer.user, company=self.operator.company)

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url, self.operator.user)
            start.is_properly_displayed()
            start.has_shareholder_count(Shareholder.objects.count())

        except Exception, e:
            self._handle_exception(e)

    def test_ticket_8(self):
        """ adding shareholder with user and userprofile for the same user for
        many companies/registers

        means we will create 3 companies, with 3 operators and each will add the
        same shareholder for its company.

        then login as the shareholder and check what happened and what is shown
        """
        ops = []
        ops.append(OperatorGenerator().generate())
        ops.append(OperatorGenerator().generate())
        ops.append(OperatorGenerator().generate())
        user = UserGenerator().generate()

        try:
            for op in ops:
                start = page.StartPage(
                    self.selenium, self.live_server_url, op.user)
                start.is_properly_displayed()
                start.has_shareholder_count(Shareholder.objects.filter(
                    company=op.company).count())
                start.click_open_add_shareholder()
                start.add_shareholder(user)
                start.click_save_add_shareholder()
                start.has_shareholder_count(Shareholder.objects.filter(
                    company=op.company).count())

            # shareholder now, no shareholder login yet
            # start = page.StartPage(
            #    self.selenium, self.live_server_url, user)
            # start.is_properly_displayed()

            time.sleep(2)
            self.assertEqual(user.shareholder_set.count(), 3)
            for op in ops:
                self.assertEqual(
                    user.shareholder_set.filter(company=op.company).count(), 1)

        except Exception, e:
            self._handle_exception(e)
