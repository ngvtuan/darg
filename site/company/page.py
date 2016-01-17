"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

import time

from django.core.urlresolvers import reverse

from shareholder.page import BasePage


class CompanyPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user, company):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        self.company = company

        # prepare driver
        super(CompanyPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username, password='test')
        self.driver.get('%s%s' % (live_server_url, reverse(
            "company", kwargs={'company_id': self.company.pk}
        )))

    # -- INPUT COMMANDs
    def enter_new_operator_email(self, email):
        el = self.driver.find_element_by_id('add-operator-form')
        form = el.find_element_by_tag_name('form')
        field = form.find_element_by_tag_name('input')

        field.send_keys(email)

    # -- CLICKs
    def click_save_new_operator(self):
        time.sleep(2)
        el = self.driver.find_element_by_id('add-operator-form')
        button = el.find_element_by_class_name(
            "btn-focus")
        button.click()

    def click_open_add_new_operator_form(self):
        button = self.driver.find_element_by_class_name(
            'toggle-add-operator-form')
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", button)
        button.click()

    def click_remove_operator(self, operator):
        table = self.driver.find_element_by_class_name(
            'operators'
        )
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", table)
        rows = table.find_elements_by_tag_name('tr')
        match = False
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            for td in tds:
                if operator.user.email in td.text:
                    match = True
            if match:
                button = row.find_element_by_class_name('remove-operator')
                button.click()
                break

    # -- VALIDATIONs
    def is_operator_displayed(self, email):
        time.sleep(1)
        return email in self.driver.page_source
