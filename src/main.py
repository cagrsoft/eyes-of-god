import os
import asyncio
import datetime
import sys
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest

load_dotenv()

EyeGodsBot = 'EyeGodsBot'

API_ID = 'TLG_API_ID'
API_HASH = 'TLG_API_HASH'

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
create_abs_path = lambda file_name : os.path.join(THIS_FOLDER, file_name)
file_name = None # contents are written in this file during the session

client = TelegramClient('eyes-of-god', os.getenv(API_ID), os.getenv(API_HASH))

def create_output_file_name():
    # if global file_name is already created in this session, then use it
    global file_name
    if file_name: return file_name

    default_file_name = 'output.txt'
    name = default_file_name

    i = 1
    while os.path.exists(create_abs_path(name)):
        name = f'{i}-{default_file_name}'
        i += 1
    
    file_name = name

    return name

async def search_contacts_from_file():
    _, input_file_name = sys.argv
    abs_path = os.path.join(THIS_FOLDER, input_file_name)
    
    with open(abs_path, 'r') as file:
        line = file.readline()
        while line:
            await client.send_message(EyeGodsBot, str(line))
            line = file.readline()
            await asyncio.sleep(1) # TODO: add some sleep not to block tlg account

@client.on(events.NewMessage(from_users=EyeGodsBot))
async def handler(event):
    msg = event.message.message
    # print(msg)

    # ignore all meta messages, except those which have 'Номер'
    if not 'Номер' in msg: return
    
    abs_path = create_abs_path(create_output_file_name())
    with open(abs_path, 'a') as file:
        lines = msg.split('\n')
        for l in lines:
            if 'Номер' in l or 'Telegram' in l or 'Email' in l:
                await file.write(msg)
                await file.write(' | ')
        await file.write('\n')
    
    # TODO client.disconnect() when all responses are back

async def main():
    await client.start()

    await search_contacts_from_file()
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('Press Ctrl+C to stop the script, if needed')
    loop.run_until_complete(main())