"""
Class to keep all app-level constants
"""


class Constants(object):
    LOGIN_WAIT_TIMEOUT_SEC = 10
    APPOINTMENT_FILE_PATH_DEFAULT = "/shared/new_appointment.txt"
    APPOINTMENT_FILE_PATH_LOCAL = "./new_appointment.txt"
    LOG_FILE_PATH = "/shared/geckodriver.log"
    APPOINTMENT_SCREENSHOT_PATH = "/shared/appointment_screenshot.png"
    EXCEPTION_SCREENSHOT_PATH = "/shared/exception_screenshot.png"
    MAIN_URL = "https://ais.usvisa-info.com/he-il/niv/users/sign_in"
    TEL_AVIV_TIMES_PATH = "appointment/days/96.json"
    ACTIONS_PAGE_PATH = "continue_actions"
    FIREFOX_BIN_PATH = "/usr/local/bin/geckodriver"
    FIREFOX_OSX_BIN_PATH = "./geckodriver"
    RESCHEDULE_TEXT_HEB = "קבע פגישה מחדש"
    MACOS_CONTEXT = 'macos'
    DEFAULT_CONTEXT = 'default'
