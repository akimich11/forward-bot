import functools
import traceback

import settings
from base.bot import bot
from users.service import UserService


def access_checker(admin_only=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(message, *args, **kwargs):
            is_user_allowed = UserService.is_user_in_db(message.from_user.id)
            is_ilya = message.from_user.id == settings.ILYA_ID
            if (admin_only and is_ilya) or (not admin_only and is_user_allowed):
                return func(message, *args, *kwargs)

            if admin_only and not is_ilya:
                bot.send_message(message.chat.id, 'Команда доступна только Илье')
            elif not admin_only and not is_user_allowed:
                bot.send_message(message.chat.id, 'Сначала подпишись, пожалуйста. Нажми /register и отправь своё имя. '
                                                  'Можешь и ненастоящее имя указать -- главное, чтобы Илья понял, '
                                                  'от кого сообщение')
        return wrapped
    return decorator


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
