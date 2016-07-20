import datetime
import time

from django.contrib.auth import get_user_model

from project.base import BaseSeleniumTestCase
from shareholder.generators import (
    UserGenerator, TwoInitialSecuritiesGenerator, OperatorGenerator
)
from shareholder.models import Company
from company import page

User = get_user_model()


# --- FUNCTIONAL TESTS
class CompanyFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)

    def test_add_new_operator(self):
        """ means: create a option plan and move options for users """

        user = UserGenerator().generate()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_open_add_new_operator_form()
            p.enter_new_operator_email(user.email)
            p.click_save_new_operator()
            self.assertTrue(
                p.is_operator_displayed(user.email)
            )
            self.assertTrue(user.operator_set.filter(
                company=self.operator.company).exists()
            )
        except Exception, e:
            self._handle_exception(e)

    def test_add_new_operator_invalid_user(self):
        """ means: create a option plan and move options for users """

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_open_add_new_operator_form()
            p.enter_new_operator_email('a@a.de')
            p.click_save_new_operator()
            self.assertFalse(
                p.is_operator_displayed('a@a.de')
            )
            self.assertFalse(User.objects.filter(email='a@a.de').exists())
        except Exception, e:
            self._handle_exception(e)

    def test_delete_operator(self):
        operator = OperatorGenerator().generate(
            company=self.operator.company)
        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_remove_operator(operator)
            self.assertFalse(
                p.is_operator_displayed(operator.user.email)
            )
            self.assertFalse(self.operator.company.operator_set.filter(
                user=operator.user).exists())
        except Exception, e:
            self._handle_exception(e)

    def test_edit_founding_date_76(self):
        """
        edit companies founding_date using the datepicker
        """
        try:

            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("founding-date")
            p.click_open_datepicker("founding-date")
            p.click_date_in_datepicker("founding-date")
            p.save_edit("founding-date")

            today = datetime.datetime.now().date()
            founding_date = datetime.date(today.year, today.month, 1)
            time.sleep(1)
            self.assertEqual(
                p.get_founding_date(),
                founding_date.strftime('%d.%m.%y'))

        except Exception, e:
            self._handle_exception(e)

        self.assertEqual(
            Company.objects.get(id=self.operator.company.id).founded_at,
            founding_date)

    def test_add_number_segment(self):

        for s in self.operator.company.security_set.all():
            s.track_numbers = True
            s.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", "88, 99-100")
            p.save_edit("security")

        except Exception, e:
            self._handle_exception(e)

        time.sleep(1)

        self.assertTrue(
            [88, u' 99-100'] in
            self.operator.company.security_set.values_list(
                'number_segments', flat=True))

    def test_alter_number_segment(self):

        security = self.operator.company.security_set.all()[0]
        security.number_segments = [1, 2]
        security.track_numbers = True
        security.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", ", 88, 99-100")
            p.save_edit("security")

        except Exception, e:
            self._handle_exception(e)

        time.sleep(1)

        self.assertTrue(
            [1, 2, 88, u' 99-100'] in
            self.operator.company.security_set.values_list(
                'number_segments', flat=True))

    def test_save_invalid_number_segment(self):

        security = self.operator.company.security_set.all()[0]
        security.number_segments = [1, 2]
        security.track_numbers = True
        security.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", ";X, 88, 99-100")
            p.save_edit("security")

        except Exception, e:
            self._handle_exception(e)

        self.assertTrue(self.selenium.find_element_by_class_name(
            'editable-error').is_displayed())

    def test_no_numbered_shares(self):
        """
        test that company without numbered shares does not see anything
        """
        try:
            page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )

        except Exception, e:
            self._handle_exception(e)

        self.assertFalse(self.selenium.find_element_by_class_name(
            'numbered-segments').is_displayed())
