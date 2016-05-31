"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

import time

from selenium.webdriver.support.ui import Select

from shareholder.generators import DEFAULT_TEST_DATA


class BasePage(object):
    """Base class to initialize the base page that will be called
    from all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(10)

    def _is_element_displayed(self, **kwargs):

        time.sleep(3)

        if kwargs.get('cls'):
            el = self.driver.find_element_by_class_name(
                kwargs.get('cls')
            )
        if kwargs.get('id'):
            el = self.driver.find_element_by_id(
                kwargs.get('id')
            )

        return el.is_displayed()

    def login(self, username, password):
        """ log the user in """
        self.driver.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        self.driver.find_element_by_xpath(
            '//*[@id="id_username"]').send_keys(username)
        self.driver.find_element_by_xpath(
            '//*[@id="id_password"]').send_keys(password)
        self.driver.find_element_by_xpath(
            '//*[@id="auth"]/form/button').click()
        page_heading = self.driver.find_element_by_tag_name(
            'h1').get_attribute('innerHTML')
        assert page_heading == 'Willkommen {}!'.format(
            username), 'failed to login. got {} page instead'.format(
            page_heading)

    def refresh(self):
        """ reload page """
        self.driver.get(self.driver.current_url)


class ShareholderDetailPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user, path=None):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(ShareholderDetailPage, self).__init__(driver)

        # login and load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username, password='test')
        if path:
            self.driver.get('%s%s' % (live_server_url, path))
        else:
            self.driver.get('%s%s' % (live_server_url))

    def click_to_edit(self, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-click')
        el.click()

    def edit_shareholder_number(self, value, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-input')
        el.clear()
        el.send_keys(str(value))

    def save_edit(self, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-buttons')
        el = el.find_element_by_tag_name('button')
        el.click()


class OptionsPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(OptionsPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username, password='test')
        self.driver.get('%s%s' % (live_server_url, '/options/'))

    # -- INPUT COMMANDs
    def enter_option_plan_form_data(self):
        el = self.driver.find_element_by_id('add_option_plan')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        select = Select(selects[0])
        select.select_by_visible_text('Preferred Stock')

        inputs[0].send_keys(DEFAULT_TEST_DATA.get('date'))
        inputs[1].send_keys(DEFAULT_TEST_DATA.get('title'))
        inputs[2].send_keys(DEFAULT_TEST_DATA.get('exercise_price'))
        inputs[3].send_keys(DEFAULT_TEST_DATA.get('share_count'))
        inputs[4].send_keys(DEFAULT_TEST_DATA.get('comment'))

    def enter_transfer_option_data(self, **kwargs):
        el = self.driver.find_element_by_id('add_option_transaction')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        inputs[0].send_keys(DEFAULT_TEST_DATA.get('date'))
        inputs[1].send_keys(DEFAULT_TEST_DATA.get('count'))
        inputs[2].send_keys(DEFAULT_TEST_DATA.get('vesting_period'))

        buyer = kwargs.get('buyer')
        seller = kwargs.get('seller')

        select_input = []
        if buyer:
            select_input.extend([buyer.user.email])
        else:
            select_input.extend([''])
        select_input.extend([DEFAULT_TEST_DATA.get('title')])
        if seller:
            select_input.extend([seller.user.email])

        for key, select in enumerate(selects):
            select = Select(select)
            if key < len(select_input) and select_input[key] != '':
                select.select_by_visible_text(select_input[key])

    # -- CLICKs
    def click_open_create_option_plan(self):
        time.sleep(2)
        el = self.driver.find_element_by_link_text(
            "Neuen Optionsplan erstellen")
        el.click()

    def click_save_option_plan_form(self):
        el = self.driver.find_element_by_id('add_option_plan')
        div = el.find_elements_by_class_name('form-group')[1]
        button = div.find_elements_by_tag_name('button')[1]
        button.click()

    def click_open_transfer_option(self):
        el = self.driver.find_element_by_link_text(u"Optionen \xfcbertragen")
        el.click()

    def click_save_transfer_option(self):
        el = self.driver.find_element_by_xpath(
            '//*[@id="add_option_transaction"]/div/form/div[2]/button[2]')
        el.click()

    # -- VALIDATIONs
    def is_option_plan_form_open(self):
        return self._is_element_displayed(id='add_option_plan')

    def is_no_errors_displayed(self):
        """ MUST not find it, hence exception is True :) """
        try:
            self._is_element_displayed(cls='alert-danger')
            return False
        except:
            return True

    def is_option_plan_displayed(self):
        h2s = self.driver.find_elements_by_tag_name('h2')
        string = u"Optionsplan: {} f\xfcr {}".format(
            DEFAULT_TEST_DATA.get('title'),
            DEFAULT_TEST_DATA.get('security'))
        for h2 in h2s:
            if h2.text == string:
                return True
        return False

    def is_transfer_option_shown(self, **kwargs):
        for table in self.driver.find_elements_by_class_name('table'):
            for td in table.find_elements_by_tag_name('td'):
                s = "{} {}".format(
                    kwargs.get('buyer').user.first_name,
                    kwargs.get('buyer').user.last_name,
                )
                if s == td.text:
                    return True
        return False

    def is_option_date_equal(self, date):
        """
        return the date from the markup to the test for verification

        date must be string
        """
        for table in self.driver.find_elements_by_class_name('table'):
            for td in table.find_elements_by_tag_name('td'):
                div = td.find_elements_by_class_name('bought-at')
                if len(div) > 0 and div[0].text == date:
                    return True
        return False

    # --  aggregations of logic
    def prepare_optionplan_fixtures(self):
        """ setup options plan """
        self.click_open_create_option_plan()

        self.enter_option_plan_form_data()
        self.click_save_option_plan_form()
