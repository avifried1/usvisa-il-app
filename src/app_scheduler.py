"""
Schedule appointment
"""
from selenium.webdriver.support.ui import Select
from emoji import emojize
from element_paths import ElementPath


class AppScheduler:
    def __init__(self, logger, browser, bot):
        self.logger = logger
        self.bot = bot
        self.browser = browser

    def schedule_app(self, earliest_appointment, new_appointment_date, chat_id):
        earliest_appointment.click()
        hours = Select(self.browser.find_element_by_xpath(ElementPath.APPOINTMENT_TIMES_XPATH))
        hour = hours.options[1].text
        self.logger.info("new earlier appointment at {0}, scheduling...".format(hour))
        hours.select_by_index(1)
        text_msg1 = ":party_popper:  Found new visa Appointment for {0}, {1}! Scheduling...".format(new_appointment_date, hour)
        self.bot.sendMessage(chat_id=chat_id, text=emojize(text_msg1))

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SUBMIT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.browser.find_elements_by_id(ElementPath.APPOINTMENT_SUBMIT_ID).click()

        self.logger.info("appointment set!")
        text_msg2 = ":thumbs_up:  Scheduled new visa Appointment for {0}, {1}".format(new_appointment_date, hour)
        self.bot.sendMessage(chat_id=chat_id, text=emojize(text_msg2))
        f = open("new_appointment.txt", "w")
        f.write(text_msg2)
        f.close()

    def dont_schedule_app(self):
        self.logger.info("appointment is after current appointment, doing nothing...")