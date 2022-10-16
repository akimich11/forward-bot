from base.bot import bot
from base.decorators import exception_handler, access_checker
from users.service import UserService, MessageService
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


@bot.message_handler(commands=['start'])
@exception_handler
def send_start_message(message):
    bot.send_message(message.chat.id, 'Привет. Можешь отправлять мне сообщения для Ильи в любом виде, я передам. '
                                      'Но сначала подпиши их, пожалуйста: нажми /register')


@bot.message_handler(commands=['register'])
def register(message):
    UserService.create_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Отправь своё имя. Можно ненастоящее, главное чтобы Илья понял, от кого')


@bot.message_handler(commands=['read'])
@exception_handler
@access_checker(admin_only=True)
def send_users_markup(message):
    users = MessageService.get_users_who_sent_greetings()
    if users is not None:
        users = [name for _, name in users]
        buttons = [InlineKeyboardButton(username, callback_data=username) for username in users]
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*buttons)
        bot.send_message(message.chat.id, 'Есть сообщения от следующих пользователей', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Пока никто ничего не написал :(')


@bot.message_handler(content_types=['text', 'photo', 'sticker', 'animation',
                                    'audio', 'document', 'video', 'voice', 'poll', 'location'])
@exception_handler
@access_checker()
def collect_message(message):
    if UserService.get_user_name(message.from_user.id) is None:
        UserService.set_user_name(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Записал имя, можешь отправлять поздравления')
    else:
        MessageService.save_message(message)
        bot.send_message(message.chat.id, 'Сообщение получено', reply_to_message_id=message.id)


@bot.callback_query_handler(lambda call: True)
@exception_handler
@access_checker(admin_only=True)
def send_greetings(call):
    user_id = UserService.get_user_id(call.data)
    greetings = MessageService.get_greeting_messages(user_id)
    bot.edit_message_text(call.message.text, call.message.chat.id, call.message.id, reply_markup=None)
    bot.send_message(call.message.chat.id, f"Поздравления от пользователя {call.data}:")
    for message_id in greetings:
        bot.forward_message(call.message.chat.id, user_id, message_id)
