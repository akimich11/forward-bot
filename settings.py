import os
from urllib.parse import urlparse

TOKEN = os.getenv('BOT_TOKEN', '5769222315:AAHnXxNBO0PV0qxjhxmHhTYq4icO3qUeSbA')

MOCK_DATABASE = os.getenv('MOCK_DATABASE', 'True') == 'True'
if MOCK_DATABASE:
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'postgres'
    DATABASE_HOST = '127.0.0.1'
    DATABASE_NAME = 'greetings'
else:
    url = urlparse(os.getenv('DATABASE_URL'))
    DATABASE_USER = url.username
    DATABASE_PASSWORD = url.password
    DATABASE_HOST = url.hostname
    DATABASE_NAME = os.getenv('DATABASE_NAME')

SUPERUSER_ID = os.getenv('SUPERUSER_ID', 270241310)
ILYA_ID = os.getenv('ILYA_ID', 270241310)
