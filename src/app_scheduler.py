"""
Schedule appointment
"""
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from emoji import emojize
from element_paths import ElementPath
from constants import Constants


class AppScheduler:
    def __init__(self, logger, browser, os, bot):
        self.logger = logger
        self.bot = bot
        self.browser = browser
        self.os = os

    def schedule_app(self, earliest_appointment, new_appointment_date, chat_id):
        earliest_appointment.click()
        hours = Select(self.browser.find_element(By.ID, ElementPath.APPOINTMENT_TIMES_ID))
        hour = hours.options[1].text
        self.logger.info("new earlier appointment at {0}, scheduling...".format(hour))
        hours.select_by_index(1)
        text_msg1 = ":party_popper:  Found new visa Appointment for {0}, {1}! Scheduling...".format(new_appointment_date, hour)
        self.bot.sendMessage(chat_id=chat_id, text=emojize(text_msg1))

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SUBMIT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.browser.find_element(By.ID, ElementPath.APPOINTMENT_SUBMIT_ID).click()
        self.browser.find_element(By.CSS_SELECTOR, ElementPath.APPOINTMENT_CONFIRMATION_CLASS).click()
        time.sleep(4)

        self.logger.info("appointment set!")
        self.browser.save_screenshot(Constants.APPOINTMENT_SCREENSHOT_PATH)
        text_msg2 = ":thumbs_up:  Scheduled new visa Appointment for {0}, {1}".format(new_appointment_date, hour)
        self.bot.sendMessage(chat_id=chat_id, text=emojize(text_msg2))
        f = open(self.get_app_filepath_by_context(self.os), "w")
        f.write(text_msg2)
        f.close()

    def dont_schedule_app(self):
        self.logger.info("appointment is after current appointment, doing nothing...")

    @staticmethod
    def get_app_filepath_by_context(os):
        if os == Constants.DEFAULT_CONTEXT:
            return Constants.APPOINTMENT_FILE_PATH_DEFAULT
        else:
            return Constants.APPOINTMENT_FILE_PATH_LOCAL
