import settings
from base.bot import bot
from base.decorators import exception_handler, access_checker
from users.service import UserService


@bot.message_handler(commands=['start'])
@exception_handler
def send_start_message(message):
    bot.send_message(message.chat.id, 'Привет. Можешь отправлять мне поздравления в любом виде, я всё передам Илье')


@bot.message_handler(commands=['read'])
@access_checker
def send_greetings(message):
    greetings = UserService.get_greeting_messages()
    gr_dict = {user_id: [] for user_id, _ in greetings}
    for user_id, text in greetings:
        gr_dict[user_id].append(text)

    bot.send_message(message.chat.id, f"Поздравления от пользователя {settings.SUPERUSER_ID}")
    for message_id in gr_dict[settings.SUPERUSER_ID]:
        bot.forward_message(message.chat.id, settings.SUPERUSER_ID, message_id)


@bot.message_handler(content_types=['text'])
@exception_handler
def collect_message(message):
    UserService.save_message(message)
    bot.send_message(message.chat.id, 'Сообщение получено')
