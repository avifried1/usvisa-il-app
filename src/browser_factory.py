"""
Get browser by environment
"""
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from constants import Constants
from pyvirtualdisplay import Display


class BrowserFactory:
    def __init__(self, logger):
        self.logger = logger

    def get_browser(self, os):
        return {
            Constants.MACOS_CONTEXT: self._osx_browser,
            Constants.DEFAULT_CONTEXT: self._default_browser
        }.get(os, Constants.DEFAULT_CONTEXT)()

    @staticmethod
    def _osx_browser():
        firefox_options = Options()
        firefox_options.headless = False
        service = Service(Constants.FIREFOX_OSX_BIN_PATH)
        return webdriver.Firefox(service=service, options=firefox_options)

    @staticmethod
    def _default_browser():
        display = Display(visible=False, size=(800, 600))
        display.start()
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options.set_preference("gfx.webrender.all", True)
        service = Service(Constants.FIREFOX_BIN_PATH, log_path=Constants.LOG_FILE_PATH)
        return webdriver.Firefox(service=service, options=firefox_options)
