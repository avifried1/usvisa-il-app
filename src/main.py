#!/usr/bin/env python
import time
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from os import path, environ
from element_paths import ElementPath
from constants import Constants
import browser_factory
import bot_null
from app_scheduler import AppScheduler
import telegram
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

if __name__ == "__main__":
    current_app_datetime = datetime(current_appointment_year, current_appointment_month, current_appointment_day)
    app_os = environ.get('app_os', Constants.DEFAULT_CONTEXT)
    if path.exists(AppScheduler.get_app_filepath_by_context(app_os)):
        log.info("new appointment already set! Exiting...")
        exit(0)
    log.info('running in {0} context'.format(app_os))
    browser = browser_factory.BrowserFactory(log).get_browser(app_os)
    browser.get(Constants.MAIN_URL)
    scheduler = AppScheduler(log, browser, app_os, bot)
    try:
        try:
            button = browser.find_element(By.XPATH, ElementPath.LOGIN_BUTTON_XPATH)
            if button is not None:
                button.click()
        except NoSuchElementException:
            log.info('Button not found, moving on...')

        log.info('Logging in {0}'.format(visa_username))

        # login screen
        browser.find_element(By.ID, ElementPath.USER_EMAIL_ID).send_keys(visa_username)
        browser.find_element(By.ID, ElementPath.USER_PASSWORD_ID).send_keys(visa_password)
        browser.find_element(By.XPATH, ElementPath.POLICY_AGREEMENT_CHECKBOX_XPATH).click()
        browser.find_element(By.XPATH, ElementPath.SIGNIN_BUTTON_XPATH).click()

        # main page
        group = WebDriverWait(browser, Constants.LOGIN_WAIT_TIMEOUT_SEC) \
            .until(ec.presence_of_element_located((By.CSS_SELECTOR, ElementPath.ACTIVE_GROUP_CARD_CLASS)))
        group.find_element(By.CSS_SELECTOR, ElementPath.CONTINUE_BUTTON_CLASS).click()

        # Navigate straight to lookup appointments times
        browser.get(
            ':'.join([
                'view-source',
                browser.current_url.replace(Constants.ACTIONS_PAGE_PATH, Constants.TEL_AVIV_TIMES_PATH)
            ])
        )
        appointments_text = browser.find_element(By.TAG_NAME, 'pre').text
        appointments_json = json.loads(appointments_text)
        earliest_date = datetime.strptime(appointments_json[0].get('date'), '%Y-%m-%d')
        log.info("current appointment date: {0}".format(current_app_datetime))
        log.info("Earliest available appointment date: {0}".format(earliest_date))

        if earliest_date < current_app_datetime:
            # Back to Actions page to set appointment!
            browser.back()
            appointments_accordion = browser.find_elements(By.CLASS_NAME, ElementPath.ACCORDION_BUTTONS_CLASS)

            appointment_reschedule = [el for el in appointments_accordion if el.text == Constants.RESCHEDULE_TEXT_HEB][0]
            appointment_reschedule.click()
            appointment_button = appointment_reschedule.find_element(By.CSS_SELECTOR, ElementPath.ACTION_BUTTONS_CLASS)
            appointment_button.click()

            # find appointment
            log.info("looking for appointment date")
            time.sleep(3)
            appointments = browser.find_elements(By.CSS_SELECTOR, ElementPath.ACTIVE_DAY_CELL_SELECTOR)

            datepicker = WebDriverWait(browser, Constants.LOGIN_WAIT_TIMEOUT_SEC) \
                .until(ec.presence_of_element_located((By.ID, ElementPath.DATE_PICKER_ID))).click()

            while len(appointments) == 0:
                log.info("no appointments! Moving to next month...")
                log.debug(appointments)
                browser.find_element(By.XPATH, ElementPath.NEXT_MONTH_XPATH).click()
                appointments = browser.find_elements(By.CSS_SELECTOR, ElementPath.ACTIVE_DAY_CELL_SELECTOR)
            earliest_appointment = appointments[0]
            day = int(earliest_appointment.find_elements(By.CSS_SELECTOR, '*')[0].text)
            month = int(earliest_appointment.get_attribute(ElementPath.DAY_CELL_MONTH_ATTRIBUTE)) + 1
            year = int(earliest_appointment.get_attribute(ElementPath.DAY_CELL_YEAR_ATTRIBUTE))
            new_appointment_date = "{0}-{1}-{2}".format(year, month, day)

            new_app_datetime = datetime(year, month, day)
            log.info("Current appointment date: {0}".format(current_app_datetime))
            log.info("Earliest available appointment date: {0}".format(new_app_datetime))

            if new_app_datetime < current_app_datetime:
                scheduler.schedule_app(earliest_appointment, new_appointment_date, chat_id)
            else:
                scheduler.dont_schedule_app()
        else:
            scheduler.dont_schedule_app()
    except Exception as e:
        log.error(e)
        browser.save_screenshot(Constants.EXCEPTION_SCREENSHOT_PATH)
    finally:
        browser.quit()
        log.info("done")
