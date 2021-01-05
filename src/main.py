import os
import asyncio
import datetime
import sys
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest

load_dotenv()

API_ID = 'TLG_API_ID'
API_HASH = 'TLG_API_HASH'

api_id = os.getenv(API_ID)
api_hash = os.getenv(API_HASH)

client = TelegramClient('anon', api_id, api_hash)
client.start()

# print(client.get_me().stringify())

curr_path, relative_path, *rest = sys.argv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.join(THIS_FOLDER, relative_path)

with open(abs_path) as file:
    line = file.readline()
    while line:
       print(line.strip())
       client.send_message('me', str(line))
       line = file.readline()