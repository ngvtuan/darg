#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""
import time
import random

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

# from selenium.webdriver.support.ui import Select

from shareholder.page import BasePage

# from shareholder.generators import DEFAULT_TEST_DATA


class StartPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(StartPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username, password='test')
        self.driver.get('%s%s' % (live_server_url, '/start/'))

    # --- ACTIONS
    def add_shareholder(self, user):
        el = self.driver.find_element_by_id('add_shareholder')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        inputs[0].send_keys(user.first_name)
        inputs[1].send_keys(user.last_name)
        inputs[2].send_keys(user.email)
        inputs[3].send_keys(random.randint(1, 6000))

    # -- CLICKs
    def click_open_add_shareholder(self):
        time.sleep(2)
        el = self.driver.find_element_by_link_text(
            "Aktionär hinzufügen")
        el.click()

    def click_save_add_shareholder(self):
        el = self.driver.find_element_by_id('add_shareholder')
        div = el.find_elements_by_class_name('form-group')[1]
        button = div.find_elements_by_tag_name('button')[1]
        button.click()

    # --- CHECKS
    def has_shareholder_count(self, count):
        return len(self.driver.find_elements_by_tag_name('tr')) == count

    def is_properly_displayed(self):
        try:
            assert self._is_element_displayed(id='shareholder_list') is True
            assert self.operator.user.username in self.driver.page_source
            assert self.operator.company.name in self.driver.page_source
            return True
        except AssertionError:
            return False
