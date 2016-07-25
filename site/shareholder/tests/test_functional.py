import unittest
import datetime
import time

from django.core.urlresolvers import reverse

from project.base import BaseSeleniumTestCase
from shareholder.models import Shareholder, Security
from shareholder.generators import (
    ShareholderGenerator, PositionGenerator,
    TwoInitialSecuritiesGenerator, OperatorGenerator,
    OptionPlanGenerator
    )
from shareholder import page


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
            time.sleep(1)
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
            birthday = datetime.date(today.year, today.month, today.day)
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
        company = self.operator.company
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=company)
        self.buyer = ShareholderGenerator().generate(company=company)
        self.seller = ShareholderGenerator().generate(company=company)
        self.seller2 = ShareholderGenerator().generate(company=company)
        # initial position for each sec
        PositionGenerator().generate(
            buyer=self.seller,
            security=self.securities[1], number_segments=[u'0-9999'],
            count=10000, seller=None)
        PositionGenerator().generate(
            buyer=self.seller,
            security=self.securities[0], number_segments=[u'0-9999'],
            count=10000, seller=None)

    def test_add(self):
        """
        add position
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

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

    def test_add_numbered_segments(self):
        """
        add position with numbered shares
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1], count=6)

        for s in self.securities:
            s.track_numbers = True
            s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue('0, 1-2, 999-1001' in self.selenium.page_source)

        except Exception, e:
            self._handle_exception(e)

    def test_add_numbered_segments_with_segment_lookup(self):
        """
        add position with numbered shares and lookup for a shareholder
        what numbers are available
        test  trigger:
        * on change for seller, security, date
        test result
        * number segments, none
        """
        # position unsaved for data seeding
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1], count=6)

        # make one of two secs with number tracking
        s = self.operator.company.security_set.get(title='C')
        s.track_numbers = True
        s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()

            # test cycle: w/ date, seller, sec
            app.enter_bought_at(position.bought_at)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_seller(position.seller)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security)
            time.sleep(2)
            self.assertTrue(app.has_available_segments_tooltip())
            self.assertEqual(app.get_segment_from_tooltip(), u'0,1-9999')

            app.refresh()
            app.click_open_add_position_form()
            # test w/ sec + seller
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_seller(position.seller)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security)
            self.assertTrue(app.has_available_segments_tooltip())

            app.refresh()
            app.click_open_add_position_form()
            # test no segs avail
            position.seller = self.seller2
            app.enter_bought_at(position.bought_at)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_seller(position.seller)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security)
            self.assertTrue(app.has_available_segments_tooltip())
            self.assertTrue(app.has_available_segments_tooltip_nothing_found())

        except Exception, e:
            self._handle_exception(e)

    def test_add_numbered_segments_invalid(self):
        """
        add position with numbered shares
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        for s in self.securities:
            s.track_numbers = True
            s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.enter_new_position_data(position)

            # clear numbers segment field
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input = form.find_elements_by_tag_name('input')[3]
            input.clear()

            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # add [A-Z] number segments
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input = form.find_elements_by_tag_name('input')[3]
            input.send_keys('AA')

            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # add valid number segments
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input.clear()
            input = form.find_elements_by_tag_name('input')[3]
            input.send_keys('1,2,3')

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
            security=self.securities[1])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()

            # enter empty data
            position.count = None
            position.value = None
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # enter data too large
            position.count = 99999999991
            position.value = 99999199999
            app.enter_new_position_data(position)
            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # working data
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

    def test_split_warning_for_numbered_shares(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_split_form()
            self.assertFalse(app.has_split_warning_for_numbered_shares())

            s = self.operator.company.security_set.get(title='C')
            s.track_numbers = True
            s.save()

            app.refresh()
            app.click_open_split_form()
            time.sleep(1)
            self.assertTrue(app.has_split_warning_for_numbered_shares())

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

            # header, row, 2x split
            self.assertEqual(app.get_position_row_count(), 3)

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
