import unittest
import datetime
import time

from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.core import mail

from project.base import BaseSeleniumTestCase
from shareholder.models import Country, Shareholder, Security, Position
from shareholder.generators import (
    ShareholderGenerator, PositionGenerator, UserGenerator,
    TwoInitialSecuritiesGenerator, OperatorGenerator, CompanyGenerator,
    ComplexShareholderConstellationGenerator, SecurityGenerator
    )
from shareholder import page


# --- MODEL TESTS
class CountryTestCase(TestCase):

    def test_model(self):

        Country.objects.create(iso_code='de', name="Germany")

        qs = Country.objects.all()
        country = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(country.iso_code, 'de')
        self.assertEqual(country.name, 'Germany')


class PositionTestCase(TransactionTestCase):

    def test_split_shares(self):
        """ share split leaves value, percent unchanged but
        increases share count per shareholder
        """
        # test data
        company = CompanyGenerator().generate(share_count=1000)
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(company=company)

        data = {
            'execute_at': datetime.datetime.now(),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        multiplier = float(data['divisor']) / float(data['dividend'])
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(),
                    'value': shareholder.share_value(),
                    'percent': shareholder.share_percent()
                }
            })

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value

        for shareholder in shareholders:
            self.assertEqual(
                shareholder.share_count(),
                round(assets[shareholder.pk]['count'] * multiplier)
            )
            self.assertEqual(
                round(shareholder.share_value()),
                assets[shareholder.pk]['value']
            )
            self.assertEqual(
                round(float(shareholder.share_percent()), 2),
                float(assets[shareholder.pk]['percent'])
            )

        self.assertEqual(
            company.share_count,
            round(company_share_count * multiplier))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )

    def test_split_shares_in_past(self):
        """
        we are splitting shares at some point in the past
        even with newer transactions entered
        approach: split in the very past and check that nothing was changed
        """
        # test data
        company = CompanyGenerator().generate(
            share_count=1000,
        )
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(
                company=company,
                company_shareholder_created_at='2013-1-1'
            )

        data = {
            'execute_at': datetime.datetime(2014, 1, 1),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        d = datetime.datetime(2014, 1, 1)
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(date=d),
                    'value': shareholder.share_value(date=d),
                    'percent': shareholder.share_percent(date=d)
                }
            })
        pcount = Position.objects.count()

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value
        cs = shareholders[0]
        mx = float(data['divisor']) / float(data['dividend'])
        for shareholder in shareholders:
            m = 1
            if shareholder.pk == cs.pk:
                m = mx
            self.assertEqual(
                shareholder.share_count(date=d),
                round(assets[shareholder.pk]['count'] * m)
            )

            # self.assertEqual(
            #     round(shareholder.share_value(date=d)),
            #     assets[shareholder.pk]['value']
            # )
            # self.assertEqual(
            #     round(float(shareholder.share_percent(date=d)), 2),
            #     float(assets[shareholder.pk]['percent'])
            # )

        self.assertEqual(
            company.share_count,
            round(company_share_count * mx))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )
        # only one new pos as no shares were basically existing as we
        # split even before company creates their first shares
        self.assertEqual(pcount + 2, Position.objects.count())

    def test_watter_split_61(self):
        """
        issue shares multiple times, sell some of them then do a split. see #61
        """
        company = CompanyGenerator().generate(share_count=10000000)
        sc = ShareholderGenerator().generate(company=company)  # aka Company
        s1 = ShareholderGenerator().generate(company=company)  # aka W
        s2 = ShareholderGenerator().generate(company=company)  # aka S
        OperatorGenerator().generate(company=company)
        security = SecurityGenerator().generate(company=company)
        now = datetime.datetime.now()
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=10000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
        )  # initial seed

        p1 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=187, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p2 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=398, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        p3 = PositionGenerator().generate(
            buyer=s2, seller=s1, count=80, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )
        p4 = PositionGenerator().generate(
            buyer=s2, seller=s1, count=437, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )
        p5 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=837, value=100, security=security,
            bought_at=now-datetime.timedelta(days=6)
            )
        p6 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=68, value=100, security=security,
            bought_at=now-datetime.timedelta(days=5)
            )

        split_data = {
            'execute_at': now - datetime.timedelta(days=4),
            'dividend': 1,
            'divisor': 100,
            'comment': "MEGA SPLIT",
            'security': security,
        }
        company.split_shares(split_data)

        p8 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=3350, value=100, security=security,
            bought_at=now-datetime.timedelta(days=3)
            )

        self.assertEqual(s1.share_count(), 100650)
        positions = Position.objects.filter(comment__contains="split").filter(
            Q(buyer=s1) | Q(seller=s1)
        )
        self.assertEqual(positions.count(), 2)
        p1 = positions[0]
        p2 = positions[1]
        self.assertEqual(p1.count, 973)
        self.assertEqual(p1.buyer, sc)
        self.assertEqual(p1.seller, s1)
        self.assertEqual(p2.count, 97300)
        self.assertEqual(p2.seller, sc)
        self.assertEqual(p2.buyer, s1)


class UserProfileTestCase(TestCase):

    def test_model(self):

        user = UserGenerator().generate()
        profile = user.userprofile

        self.assertEqual(profile.country.iso_code, 'de')
        self.assertEqual(profile.country.name, 'Germany')
        self.assertEqual(profile.province, 'Some Province')


class ShareholderTestCase(TestCase):

    fixtures = ['initial.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_index(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)

    def test_validate_gafi(self):
        """ test the gafi validation """

        # --- invalid street
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        shareholder.user.userprofile.street = ''
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # --- invalid company name
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        shareholder.user.userprofile.company_name = None
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # --- valid data
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertTrue(shareholder.validate_gafi()['is_valid'])

    def test_validate_gafi_with_missing_userprofile(self):
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        profile = shareholder.user.userprofile
        profile.delete()

        shareholder = Shareholder.objects.get(id=shareholder.id)
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertFalse(hasattr(shareholder.user, 'userprofile'))
        self.assertFalse(shareholder.validate_gafi()['is_valid'])

    def test_shareholder_detail(self):
        """ test detail view for shareholder """

        shareholder = ShareholderGenerator().generate()

        response = self.client.login(
            username=shareholder.user.username, password="test")
        self.assertTrue(response)

        response = self.client.get(
            reverse("shareholder", args=(shareholder.id,)))

        self.assertEqual(response.status_code, 200)

    def test_share_percent(self):
        shareholder = ShareholderGenerator().generate()
        PositionGenerator().generate(buyer=shareholder)

        res = shareholder.share_percent()

        self.assertEqual(res, '100.00')


# --- FUNCTIONAL TESTS
class ShareholderDetailFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def tearDown(self):
        Security.objects.all().delete()

    def test_edit_shareholder_number_53(self):
        """ means: create a option plan and move options for users """
        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'shareholder_id': self.buyer.id}
                    )
                )
            p.click_to_edit("shareholder-number")
            time.sleep(1)
            p.edit_shareholder_number(99, "shareholder-number")
            time.sleep(1)
            p.save_edit("shareholder-number")
            time.sleep(1)

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(shareholder.number, str(99))


class OptionsFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def tearDown(self):
        Security.objects.all().delete()

    def test_base_use_case(self):
        """ means: create a option plan and move options for users """

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_create_option_plan()

            self.assertTrue(app.is_option_plan_form_open())

            app.enter_option_plan_form_data()
            app.click_save_option_plan_form()

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_option_plan_displayed())

            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                buyer=self.buyer, seller=self.seller)
            app.click_save_transfer_option()

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(
                buyer=self.buyer, seller=self.seller
            ))
        except Exception, e:
            self._handle_exception(e)

    def test_base_use_case_no_buyer(self):
        """ test that options transfer form is working properly
        if there is no buyer selected """

        app = page.OptionsPage(
            self.selenium, self.live_server_url, self.operator.user)
        app.prepare_optionplan_fixtures()

        self.assertTrue(app.is_option_plan_displayed())

        app.click_open_transfer_option()
        app.enter_transfer_option_data(seller=self.seller)
        app.click_save_transfer_option()

        self.assertFalse(app.is_no_errors_displayed())

    def test_base_use_case_no_seller(self):
        """ test that options transfer form is working properly
        if there is no seller selected """

        app = page.OptionsPage(
            self.selenium, self.live_server_url, self.operator.user)
        app.prepare_optionplan_fixtures()

        self.assertTrue(app.is_option_plan_displayed())

        app.click_open_transfer_option()
        app.enter_transfer_option_data(buyer=self.buyer)
        app.click_save_transfer_option()

        self.assertFalse(app.is_no_errors_displayed())

    @unittest.skip('not implemented')
    def test_base_use_case_no_count(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_no_bougth_at(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_no_option_plan(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_same_buyer_seller(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_negative_count(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_negative_Vesting(self):
        pass
