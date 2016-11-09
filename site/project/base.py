import os
import datetime
import traceback
import inspect

from django.test import LiveServerTestCase
from django.core.mail import EmailMessage, get_connection

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display


class BaseSeleniumTestCase(LiveServerTestCase):

    def _screenshot(self):
        filename = 'screenshot_{}.png'.format(datetime.datetime.now())
        self.selenium.save_screenshot(filename)
        caller = inspect.stack()[2][3]

        # in test env its using locmem backend
        email = EmailMessage(
            subject='[darg] FE Test failed w/ %s' % caller,
            body='FE Test failed. See attached screenshot\n\n'
            'stacktrace:\n\n%s\n\nbrowser log:\n%s\n\nurl: %s' % (
                traceback.format_exc(),
                self.selenium.get_log('browser'),
                self.selenium.current_url
            ),
            from_email='no-reply@das-aktienregister.ch',
            to=('jirka.schaefer@tschitschereengreen.com',),
            connection=get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend'),
        )
        email.attach_file(filename)
        email.send()
        print "Email with Screenshot was sent..."
        os.remove(filename)

    def _handle_exception(self, e):
        """ on error print JS console of browser and also make a screenshot"""
        # print browser console
        for entry in self.selenium.get_log('browser'):
            print entry

        # print python exception
        print u"Python Exception: {}".format(e), traceback.format_exc()

        self._screenshot()  # make screenshot

        # reraise Exc
        raise

    @classmethod
    def setUpClass(cls):
        # debug options
        # options = webdriver.ChromeOptions()
        # options.binary_location = '/usr/bin/google-chrome'
        # service_log_path = "./chromedriver.log"
        # service_args = ['--verbose']

        # Add following 2 line before start the Chrome
        display = Display(visible=0, size=(1024, 768))
        display.start()

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        cls.selenium = WebDriver(
            os.path.join(os.getcwd(), 'chromedriver'),
            chrome_options=chrome_options)

        cls.selenium.implicitly_wait(10)
        super(BaseSeleniumTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BaseSeleniumTestCase, cls).tearDownClass()
