# For testing only
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from os import path, environ
from element_paths import ElementPath
from constants import Constants
import bot_null
import app_scheduler
import telegram
import time
import logging

# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger('usvisa')

# Config
current_appointment_year = int(environ.get('current_appointment_year', '2222'))
current_appointment_month = int(environ.get('current_appointment_month', '12'))
current_appointment_day = int(environ.get('current_appointment_day', '31'))
visa_username = environ.get('visa_creds_username')
visa_password = environ.get('visa_creds_password')
telegram_token = environ.get('telegram_token')
chat_id = environ.get('telegram_chat_id')

if telegram_token is not None:
    bot = telegram.Bot(token=telegram_token)
else:
    bot = bot_null.BotNull(log)


def get_browser():
    firefox_options = Options()
    firefox_options.headless = False
    service = Service(Constants.FIREFOX_OSX_BIN_PATH)
    return webdriver.Firefox(service=service, options=firefox_options)


if __name__ == "__main__":
    if path.exists(Constants.APPOINTMENT_FILE_PATH):
        log.info("new appointment already set! Exiting...")
        exit(0)
    browser = get_browser()
    browser.get(Constants.MAIN_URL)
    scheduler = app_scheduler.AppScheduler(log, browser, bot)
    try:
        try:
            button = browser.find_element(By.XPATH, ElementPath.LOGIN_BUTTON_XPATH)
            if button is not None:
                button.click()
        except NoSuchElementException:
            log.info('Button not found, moving on...')

        log.info('Logging in {0}'.format(visa_username))
        # login
        browser.find_element(By.ID, ElementPath.USER_EMAIL_ID).send_keys(visa_username)
        browser.find_element(By.ID, ElementPath.USER_PASSWORD_ID).send_keys(visa_password)
        browser.find_element(By.XPATH, ElementPath.POLICY_AGREEMENT_CHECKBOX_XPATH).click()
        browser.find_element(By.XPATH, ElementPath.SIGNIN_BUTTON_XPATH).click()

        # find appointment
        log.info("looking for an appointment date")
        time.sleep(3)
        datepicker = browser.find_element(By.ID, ElementPath.DATE_PICKER_ID).click()
        appointments = browser.find_elements(By.CSS_SELECTOR, ElementPath.ACTIVE_DAY_CELL_SELECTOR)
        while len(appointments) == 0:
            log.info("no appointments! Moving to next month...")
            log.debug(appointments)
            browser.find_element(By.XPATH, ElementPath.NEXT_MONTH_XPATH).click()
            appointments = browser.find_elements(By.CSS_SELECTOR, ElementPath.ACTIVE_DAY_CELL_SELECTOR)
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