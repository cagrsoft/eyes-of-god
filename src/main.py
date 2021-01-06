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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
EyeGodsBot = 'EyeGodsBot'

# TODO change 'anon' to 'eyes-of-god'
client = TelegramClient('eyes-of-god', api_id, api_hash)

async def search_contacts_from_file():
    _, file_name, *rest = sys.argv
    abs_path = os.path.join(THIS_FOLDER, file_name)
    
    with open(abs_path, 'r') as file:
        line = file.readline()
        while line:
            await client.send_message(EyeGodsBot, str(line))
            line = file.readline()
            await asyncio.sleep(1) # TODO: add some sleep not to block tlg account

async def main():
    await client.start()
    await search_contacts_from_file()
    await client.run_until_disconnected()
    # TODO client.disconnect() when all responses are back

# print(client.get_me().stringify())

@client.on(events.NewMessage(from_users=EyeGodsBot))
async def handler(event):
    # print(event.message.message)
    abs_path = os.path.join(THIS_FOLDER, 'output.txt')
    with open(abs_path, 'a') as file:
        msg = event.message.message
        print(msg)
        lines = msg.split('\n')
        only_needed_data = [l for l in lines if 'Номер' in l or 'Telegram' in l or 'Email' in l]
        await file.write('—'.join(only_needed_data))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('Press Ctrl+C to stop the script, if needed')
    loop.run_until_complete(main())