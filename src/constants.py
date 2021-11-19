"""
Class to keep all app-level constants
"""


class Constants(object):
    LOGIN_WAIT_TIMEOUT_SEC = 10
    APPOINTMENT_FILE_PATH = "/shared/new_appointment.txt"
    LOG_FILE_PATH = "/shared/geckodriver.log"
    APPOINTMENT_SCREENSHOT_PATH = "/shared/appointment_screenshot.png"
    EXCEPTION_SCREENSHOT_PATH = "/shared/exception_screenshot.png"
    MAIN_URL = "https://ais.usvisa-info.com/he-il/niv/users/sign_in"
    FIREFOX_BIN_PATH = "/usr/local/bin/geckodriver"
    FIREFOX_OSX_BIN_PATH = "./geckodriver"
    RESCHEDULE_TEXT_HEB = "קבע פגישה מחדש"
