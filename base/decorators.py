import functools
import traceback

import settings
from base.bot import bot
from users.service import UserService


def access_checker(func):
    @functools.wraps(func)
    def wrapped(message, *args, **kwargs):
        if message.from_user.id != settings.SUPERUSER_ID:
            bot.send_message(message.chat.id, 'Команда доступна только Илье')
        else:
            return func(message, *args, *kwargs)

    return wrapped


def exception_handler(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return result
        except BaseException:
            bot.send_message(settings.SUPERUSER_ID, 'Unexpected error:\n' + traceback.format_exc())
            if len(args):
                if hasattr(args[0], 'message'):
                    chat_id = args[0].message.chat.id
                else:
                    chat_id = args[0].chat.id
                bot.send_message(chat_id, 'Unexpected error')
            return None

    return wrapped
