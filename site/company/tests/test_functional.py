from django.test import TestCase
from django.contrib.auth import get_user_model

from project.base import BaseSeleniumTestCase
from shareholder.generators import (
    UserGenerator, TwoInitialSecuritiesGenerator, OperatorGenerator
)
from company import page

User = get_user_model()

# --- MODEL TESTS


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
