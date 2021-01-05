import os
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync

load_dotenv()

API_ID = 'API_ID'
API_HASH = 'API_HASH'

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = os.getenv(API_ID) # TODO: use this from process.env
api_hash = os.getenv(API_HASH) # TODO: use this from process.env

client = TelegramClient('anon', api_id, api_hash)
client.start()

# print(client.get_me().stringify())

client.send_message('me', 'Test')