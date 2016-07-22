"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

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

    def use_datepicker(self, class_name, date):
        """
        use default datepicker to select a date
        """
        self.click_open_datepicker(class_name)
        self.click_date_in_datepicker(class_name)

    def click_open_datepicker(self, class_name):
        """
        click to open the datepicker for element X
        """
        el = self.driver.find_element_by_class_name(class_name)
        btns = el.find_elements_by_xpath(
            '//*[contains(@class, "date-field")]//'
            'span[@class="input-group-btn"]//button'
        )
        for btn in btns:
            if btn.is_displayed():
                btn.click()
                return

        raise Exception('Clickable button not found')

    def click_date_in_datepicker(self, class_name):
        """
        select some date in datepicker

        click first day of current month
        """
        el = self.driver.find_element_by_class_name(class_name)
        dp_rows = el.find_elements_by_xpath(
            '//table[@class="uib-daypicker"]//tr[@class="uib-weeks ng-scope"]')
        # in case we have multiple dps
        for dp_row in dp_rows:
            if not dp_row.is_displayed():
                continue

            for td in dp_row.find_elements_by_tag_name('td'):
                el2 = td.find_elements_by_tag_name('span')
                if el2 and el2[0].text == '01':
                    btn = td.find_element_by_tag_name('button')
                    btn.click()
                    return

        raise Exception('Clickable button not found')

    def is_no_errors_displayed(self):
        """ MUST not find it, hence exception is True :) """
        try:
            self._is_element_displayed(cls='alert-danger')
            return False
        except:
            return True

    def scroll_to(self, Y=None, element=None):
        """
        scroll to element or coordinate
        """
        if element:
            self.driver.execute_script(
                "return arguments[0].scrollIntoView();", element)
        else:
            self.driver.execute_script("window.scrollTo(0, {})".format(Y))

    def wait_until_clickable(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable(element))
        return element

    def wait_until_visible(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, 10)
        if isinstance(element, WebElement):
            element = wait.until(EC.visibility_of(element))
        else:
            element = wait.until(EC.visibility_of_element_located(element))
        return element

    def wait_until_invisible(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.invisibility_of_element_located(element))
        return element

    def wait_unti_text_present(self, element, text):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.text_to_be_present_in_element(element, text))
        return element

    def drag_n_drop(self, object, target):
        """
        used to simulate drag'n drop to move elemens
        from
        http://stackoverflow.com/questions/29381233/how-to-simulate-html5-drag-and-drop-in-selenium-webdriver/29381532#29381532
        object, target : jquery identifiers
        """

        jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"

        # load jQuery helper
        with open("jquery_load_helper.js") as f:
            load_jquery_js = f.read()

        # load drag and drop helper
        with open("drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()

        # load jQuery
        self.driver.execute_async_script(load_jquery_js, jquery_url)

        # perform drag&drop
        self.driver.execute_script(
            drag_and_drop_js +
            "$('{}').simulateDragDrop({ dropTarget: '{}'});".format(
                object, target
            )
        )


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
        el = self.wait_until_visible((
            By.XPATH,
            '//tr[contains(@class, "{}")]//'
            'span[contains(@class, "editable-click")]'.format(class_name)
        ))
        el.click()

    def edit_shareholder_number(self, value, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-input')
        el.clear()
        el.send_keys(str(value))

    # --- GET DATA
    def get_birthday(self, class_name="birthday"):
        """
        return date from inside this element
        """
        bday = self.driver.find_element_by_xpath(
            '//tr[@class="birthday active"]/td/span')
        return bday.text

    # --- trigger buttons
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

        inputs[0].send_keys(
            kwargs.get('date') or DEFAULT_TEST_DATA.get('date'))
        inputs[1].send_keys(DEFAULT_TEST_DATA.get('count'))
        inputs[2].send_keys(DEFAULT_TEST_DATA.get('vesting_period'))

        buyer = kwargs.get('buyer')
        seller = kwargs.get('seller')

        select_input = []
        if buyer:
            select_input.extend([buyer.user.email])
        else:
            select_input.extend([''])
        select_input.extend([
            kwargs.get('title') or DEFAULT_TEST_DATA.get('title')
        ])
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
                s = u"{} {}".format(
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


class PositionPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(PositionPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username, password='test')
        self.driver.get('%s%s' % (live_server_url, '/positions/'))

    def click_confirm_position(self):
        table = self.driver.find_element_by_tag_name('table')
        time.sleep(1)
        trs = table.find_elements_by_tag_name('tr')
        row = trs[2]
        td = row.find_elements_by_tag_name('td')[-1]
        td.find_elements_by_tag_name('a')[1].click()

    def click_delete_position(self):
        table = self.driver.find_element_by_tag_name('table')
        time.sleep(1)
        trs = table.find_elements_by_tag_name('tr')
        row = trs[2]
        td = row.find_elements_by_tag_name('td')[-1]
        td.find_element_by_tag_name('a').click()

    def click_open_add_position_form(self):
        btn = self.driver.find_element_by_class_name('add-position')
        btn.click()

    def click_open_split_form(self):
        btn = self.driver.find_element_by_class_name('split-shares')
        btn.click()

    def click_open_cap_increase_form(self):
        btn = self.driver.find_element_by_class_name('add-capital')
        btn.click()

    def click_save_cap_increase(self):
        btn = self.driver.find_element_by_class_name('save-capital')
        btn.click()

    def click_save_position(self):
        btn = self.driver.find_element_by_class_name('save-position')
        btn.click()

    def click_save_split(self):
        btn = self.driver.find_element_by_class_name('save-split')
        btn.click()

    def enter_new_position_data(self, position):
        el = self.driver.find_element_by_id('add_position')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        # select elements: seller, buyer, security - before inputs to have magic
        # working
        time.sleep(2)
        for select in selects:
            select = Select(select)
            select.select_by_index(1)

        time.sleep(1)

        # input #0 use datepicker
        self.use_datepicker('add-position-form', None)
        if position.count:
            inputs[1].clear()  # clear existing values
            inputs[1].send_keys(position.count)  # count
        if position.value:
            inputs[2].clear()  # clear existing values
            inputs[2].send_keys(position.value)  # price

        # if numbered shares enter segment
        if position.security.track_numbers:
            input = form.find_elements_by_tag_name('input')[3]
            input.send_keys('0,1,2,999-1001')
            inputs[4].clear()  # clear existing values
            inputs[4].send_keys(position.comment)  # comment
        else:
            inputs[4].clear()  # clear existing values
            inputs[4].send_keys(position.comment)  # comment

    def enter_new_cap_data(self, position):

        el = self.driver.find_element_by_id('add_capital')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        # input #0 use datepicker
        self.use_datepicker('add-capital-form', None)
        if position.count:
            inputs[1].clear()
            inputs[1].send_keys(position.count)  # count
        if position.value:
            inputs[2].clear()
            inputs[2].send_keys(position.value)  # price
        inputs[3].clear()
        inputs[3].send_keys(position.comment)  # comment

        # select elements: seller, buyer, security
        for select in selects:
            select = Select(select)
            select.select_by_index(1)

    def enter_new_split_data(self, *args):
        el = self.driver.find_element_by_id('split-shares')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        # input #0 use datepicker
        self.use_datepicker('split-shares-form', None)
        inputs[1].send_keys(args[0])  # dividend
        inputs[2].send_keys(args[1])  # divisor
        inputs[3].send_keys(args[2])  # comment

        # select elements: seller, buyer, security
        for select in selects:
            select = Select(select)
            select.select_by_index(1)

    def get_position_row_data(self):
        """
        return list of data from position in single row of table
        """
        table = self.driver.find_element_by_tag_name('table')
        time.sleep(1)
        trs = table.find_elements_by_tag_name('tr')
        row = trs[2]
        return [td.text for td in row.find_elements_by_tag_name('td')]

    def get_position_row_count(self):
        table = self.driver.find_element_by_tag_name('table')
        time.sleep(1)
        trs = table.find_elements_by_tag_name('tr')
        return len(trs)

    def count_draft_mode_items(self):
        table = self.driver.find_element_by_tag_name('table')
        time.sleep(1)
        trs = table.find_elements_by_tag_name('tr')
        row = trs[2]
        return row.find_element_by_tag_name('td').text.count('Entwurf')
