import os
import asyncio
import datetime
import sys
import tools
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest

load_dotenv()

EyeGodsBot = 'EyeGodsBot'

API_ID = 'TLG_API_ID'
API_HASH = 'TLG_API_HASH'

_, input_file_name = sys.argv
abs_path_to_input_file = tools.create_abs_path(input_file_name)
abs_path_to_output_file = tools.create_abs_path(tools.create_output_file_name())
contacts_left_to_search = tools.get_line_count_in_file(abs_path_to_input_file)    

client = TelegramClient('eyes-of-god', os.getenv(API_ID), os.getenv(API_HASH))

async def search_contacts_from_file():
    try:
        with open(abs_path_to_input_file, 'r') as file:
            line = file.readline()
            while line:
                await client.send_message(EyeGodsBot, str(line))
                line = file.readline()
                await asyncio.sleep(1) # TODO: add some sleep not to block tlg account
    except Exception as e:
        print('Error:', str(e))

@client.on(events.NewMessage(from_users=EyeGodsBot))
async def handler(event):
    msg = event.message.message
    # print(msg)

    # ignore all messages, except those which have 'Номер'
    if not 'Номер' in msg: return

    try:
        with open(abs_path_to_output_file, 'a+') as file: file.write(msg)
    except Exception as e:
        print('Error:', str(e))

    # disconnect when all responses are received and no contacts left to search
    global contacts_left_to_search
    print(contacts_left_to_search)
    contacts_left_to_search -= 1
    if contacts_left_to_search == 0: await client.disconnect()

async def main():
    try:
        await client.start()
        await search_contacts_from_file()
        await client.run_until_disconnected()
    except:
        await client.disconnect()
        print('OMG!! 😱😱 Something went wrong! Okey, don\'t panic, just try one more time')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('Press Ctrl+C to stop the script, if needed')
    loop.run_until_complete(main())