from base.bot import bot
from base.decorators import exception_handler, access_checker
from users.service import UserService, MessageService
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


@bot.message_handler(commands=['start'])
@exception_handler
def send_start_message(message):
    bot.send_message(message.chat.id, 'Привет. Пока ты был на зоне, я собирал сообщения для тебя. '
                                      'Чтобы их прочитать, напиши /read')


@bot.message_handler(commands=['read'])
@exception_handler
@access_checker(admin_only=True)
def send_users_markup(message):
    users = MessageService.get_users_who_sent_greetings()
    if users is not None:
        buttons = [InlineKeyboardButton(username, callback_data=str(user_id)) for user_id, username in users]
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*buttons)
        bot.send_message(message.chat.id, 'Есть сообщения от следующих пользователей', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Пока никто ничего не написал :(')


@bot.callback_query_handler(lambda call: True)
@exception_handler
@access_checker(admin_only=True)
def send_greetings(call):
    user_id = int(call.data)
    username = UserService.get_user_name(user_id)
    greetings = MessageService.get_greeting_messages(user_id)
    bot.edit_message_text(call.message.text, call.message.chat.id, call.message.id, reply_markup=None)
    bot.send_message(call.message.chat.id, f"Сообщения от пользователя {username}:")
    for message_id in greetings:
        bot.forward_message(call.message.chat.id, user_id, message_id)
