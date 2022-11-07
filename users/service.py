from telebot.types import Message
from base import db


class MessageService(db.ConnectionMixin):
    @classmethod
    @db.get_cursor
    def save_message(cls, message: Message, cursor):
        cursor.execute("INSERT INTO ilya_messages (user_id, message_id, sent_at) VALUES (%s, %s, to_timestamp(%s))",
                       (message.chat.id,
                        message.id,
                        message.date))

    @classmethod
    @db.fetch(return_type='all_values')
    def get_greeting_messages(cls, user_id, cursor):
        cursor.execute("SELECT message_id FROM ilya_messages WHERE user_id=(%s) ORDER BY sent_at", (user_id,))

    @classmethod
    @db.fetch(return_type='all_tuples')
    def get_users_who_sent_greetings(cls, cursor):
        cursor.execute("SELECT DISTINCT u.id, name FROM ilya_messages JOIN ilya_users u "
                       "ON u.id = ilya_messages.user_id ")


class UserService(db.ConnectionMixin):
    @classmethod
    @db.get_cursor
    def is_user_in_db(cls, user_id, cursor):
        cursor.execute("SELECT * FROM ilya_users WHERE id=(%s)", (user_id,))
        user = cursor.fetchone()
        return user is not None

    @classmethod
    @db.get_cursor
    def create_user(cls, user_id, cursor):
        cursor.execute("INSERT INTO ilya_users (id, name) VALUES (%s, null) ON CONFLICT (id) DO "
                       "UPDATE SET name=null", (user_id,))

    @classmethod
    @db.fetch(return_type='value')
    def get_user_name(cls, user_id, cursor):
        cursor.execute("SELECT name FROM ilya_users WHERE id=(%s)", (user_id,))

    @classmethod
    @db.get_cursor
    def set_user_name(cls, user_id, user_name, cursor):
        cursor.execute("UPDATE ilya_users SET name=(%s) WHERE id=(%s)", (user_name, user_id))

    @classmethod
    @db.fetch(return_type='value')
    def get_user_id(cls, user_name, cursor):
        cursor.execute("SELECT id FROM ilya_users WHERE name=(%s)", (user_name,))
