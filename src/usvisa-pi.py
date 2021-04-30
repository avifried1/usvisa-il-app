# TODO: Needs further work and testing

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from datetime import datetime
from os import path
from element_paths import ElementPath
import bot_null
import app_scheduler
import telegram
import time
import logging
import yaml
from pyvirtualdisplay import Display

display = Display(visible=False, size=(800, 600))
display.start()


def get_browser(binary=None):
    firefox_options = Options()
    firefox_options.headless = True
    firefox_options.set_preference("gfx.webrender.all", True)
    return webdriver.Firefox(firefox_binary=binary, firefox_options=firefox_options)

# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('usvisa')

# Config
config = {}
with open(path.join(path.dirname(__file__), '..', 'conf/config.yaml'), 'r') as stream:
    try:
        module_config = yaml.safe_load(stream)
        config = module_config.get('usvisa')
    except yaml.YAMLError as exc:
        log.info(exc)
        exit(1)

current_appointment = config.get('current_appointment')
current_appointment_year = current_appointment.get('year', '2222')
current_appointment_month = current_appointment.get('month', '12')
current_appointment_day = current_appointment.get('day', '31')
visa_creds = config.get('visa-credentials')
visa_username = visa_creds.get('username')
visa_password = visa_creds.get('password')
telegram_config = config.get('telegram', {})
telegram_token = telegram_config.get('token')
chat_id = telegram_config.get('chat-id')
ff = config.get('firefox-path-mac')
url = config.get('visa-app-url')

browser = None
firefox_binary = FirefoxBinary(ff)
if telegram_token is not None:
    bot = telegram.Bot(token=telegram_token)
else:
    bot = bot_null.BotNull(log)


if __name__ == "__main__":
    if path.exists("new_appointment.txt"):
        log.info("new appointment already set! Exiting...")
        exit(0)
    browser = get_browser(binary=firefox_binary)
    browser.get(url)
    scheduler = app_scheduler.AppScheduler(log, browser, bot)
    try:
        button = browser.find_element_by_xpath(ElementPath.LOGIN_BUTTON_XPATH)
        if button is not None:
            button.click()

        log.info('Logging in {0}'.format(visa_username))
        # login
        browser.find_element_by_id(ElementPath.USER_EMAIL_ID).send_keys(visa_username)
        browser.find_element_by_id(ElementPath.USER_PASSWORD_ID).send_keys(visa_password)
        browser.find_element_by_xpath(ElementPath.POLICY_AGREEMENT_CHECKBOX_XPATH).click()
        browser.find_element_by_xpath(ElementPath.SIGNIN_BUTTON_XPATH).click()

        # find appointment
        log.info("looking for an appointment date")
        time.sleep(3)
        datepicker = browser.find_element_by_id(ElementPath.DATE_PICKER_ID).click()
        appointments = browser.find_elements_by_css_selector(ElementPath.ACTIVE_DAY_CELL_SELECTOR)
        while len(appointments) == 0:
            log.info("no appointments! Moving to next month...")
            log.debug(appointments)
            browser.find_element_by_xpath(ElementPath.NEXT_MONTH_XPATH).click()
            appointments = browser.find_elements_by_css_selector(ElementPath.ACTIVE_DAY_CELL_SELECTOR)
        earliest_appointment = appointments[0]
        day = int(earliest_appointment.find_elements_by_css_selector('*')[0].text)
        month = int(earliest_appointment.get_attribute(ElementPath.DAY_CELL_MONTH_ATTRIBUTE)) + 1
        year = int(earliest_appointment.get_attribute(ElementPath.DAY_CELL_YEAR_ATTRIBUTE))
        new_appointment_date = "{0}-{1}-{2}".format(year, month, day)
        current_app_datetime = datetime(current_appointment_year, current_appointment_month, current_appointment_day)
        new_app_datetime = datetime(year, month, day)
        log.info("found appointments! Earliest date: {0}".format(new_appointment_date))
        log.info("current appointment: {0}".format(current_app_datetime))
        log.info("new appointment: {0}".format(new_app_datetime))

        if new_app_datetime < current_app_datetime:
            scheduler.schedule_app(earliest_appointment, new_appointment_date, chat_id)
        else:
            scheduler.dont_schedule_app()
    finally:
        browser.quit()
        log.info("done")