"""
Null object for Telegram bot
"""


class BotNull:
    def __init__(self, logger):
        self.logger = logger

    def sendMessage(self, chat_id, text):
        self.logger.info("Skipping Telegram since no configuration was found")