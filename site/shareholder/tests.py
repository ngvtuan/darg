import unittest
import datetime
import time
from decimal import Decimal

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
    ComplexShareholderConstellationGenerator, SecurityGenerator,
    OptionPlanGenerator
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
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=80, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=437, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=837, value=100, security=security,
            bought_at=now-datetime.timedelta(days=6)
            )
        PositionGenerator().generate(
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

        PositionGenerator().generate(
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
        """
        proper share percent math
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        s2 = ShareholderGenerator().generate(company=company)
        s3 = ShareholderGenerator().generate(company=company)
        now = datetime.datetime.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=5000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        PositionGenerator().generate(
            buyer=s3, seller=sc, count=50, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )

        self.assertEqual(s1.share_percent(), '99.00')
        self.assertEqual(s2.share_percent(), '0.99')
        self.assertEqual(s3.share_percent(), '0.01')

        PositionGenerator().generate(
            buyer=s2, seller=s1, count=250000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )

        self.assertEqual(s1.share_percent(), '49.50')

    def test_share_value(self):
        """
        share value is last trated price
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        now = datetime.datetime.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=1, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        p = PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p.value = None
        p.save()

        self.assertEqual(s1.share_value(), Decimal('500000.0000'))


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
            p.edit_shareholder_number(99, "shareholder-number")
            p.save_edit("shareholder-number")
            time.sleep(1)

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(shareholder.number, str(99))

    def test_edit_birthday_76(self):
        """
        edit shareholders birthday using the datepicker
        """
        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'shareholder_id': self.buyer.id}
                    )
                )
            p.click_to_edit("birthday")
            p.click_open_datepicker("birthday")
            p.click_date_in_datepicker("birthday")
            p.save_edit("birthday")

            today = datetime.datetime.now().date()
            birthday = datetime.date(today.year, today.month, 1)
            time.sleep(1)
            self.assertEqual(
                p.get_birthday(),
                birthday.strftime('%d.%m.%y'))

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(
            shareholder.user.userprofile.birthday, birthday)


class OptionsFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=self.operator.company)
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
            self.assertTrue(app.is_option_date_equal('13.05.16'))

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

    def test_date_save_error_78(self):
        """
        for some date the server stores the day before, for some not
        good: 1.11.2016
        bad: 15.5.2016)
        """

        self.optionplan = OptionPlanGenerator().generate(
            company=self.operator.company,
            security=self.securities[0]
        )

        try:

            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                date='13. Mai 2016', buyer=self.buyer,
                title=self.optionplan.title,
                seller=self.operator.company.get_company_shareholder()
            )
            app.click_save_transfer_option()

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(buyer=self.buyer))
            self.assertTrue(app.is_option_date_equal('13.05.16'))

            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                date='1. Nov. 2016', buyer=self.buyer,
                title=self.optionplan.title,
                seller=self.operator.company.get_company_shareholder()
            )
            app.click_save_transfer_option()

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(buyer=self.buyer))
            self.assertTrue(app.is_option_date_equal('1.11.16'))

        except Exception, e:
            self._handle_exception(e)


class PositionFunctionalTestCase(BaseSeleniumTestCase):
    """
    test all core position funcs
    logic is tested in api, this here covers mainly FE logic
    """

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def test_add(self):
        """
        add position
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_add_error(self):
        """
        confirm form error handling
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()

            # enter missing
            position.count = None
            position.value = None
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # enter large data
            position.count = 99999999991
            position.value = 99999199999
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # complete data
            position.count = 999999999
            position.value = 11111111
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_cap_increase(self):
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_cap_increase_form()
            app.enter_new_cap_data(position)
            app.click_save_cap_increase()

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_split(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])
        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_split_form()
            app.enter_new_split_data(2, 3, 'test comment')
            app.click_save_split()

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_delete(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_delete_position()

            self.assertEqual(app.get_position_row_count(), 1)

        except Exception, e:
            self._handle_exception(e)

    def test_confirm(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_confirm_position()

            self.assertEqual(app.count_draft_mode_items(), 0)

        except Exception, e:
            self._handle_exception(e)
