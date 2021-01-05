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
client = TelegramClient('anon', api_id, api_hash)

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
    abs_path = os.path.join(THIS_FOLDER, 'result.txt')
    with open(abs_path, 'a') as file:
        lines = event.message.message.slit('\n')
        print('lines')
        only_needed_data = [l for l in lines if 'Номер' in l]
        print('only_needed_data', only_needed_data)
        await file.write(f'{only_needed_data}\n')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('Press Ctrl+C to stop the script')
    loop.run_until_complete(main())