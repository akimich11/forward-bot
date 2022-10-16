from telebot import TeleBot
import settings


class MdaBot(TeleBot):
    pass


bot = MdaBot(token=settings.TOKEN)
