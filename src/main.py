import os
import asyncio
import datetime
import sys
import tools
import re
import xlsxwriter
from dotenv import load_dotenv
from telethon import TelegramClient, events, sync
from telethon.tl.functions.users import GetFullUserRequest

load_dotenv()

EyeGodsBot = "EyeGodsBot"

API_ID = "TLG_API_ID"
API_HASH = "TLG_API_HASH"

api_id = tools.get_or_create_dotenv_var(API_ID)
api_hash = tools.get_or_create_dotenv_var(API_HASH)

abs_path_to_input_file = tools.create_abs_path("input.txt")
abs_path_to_output_file = tools.create_abs_path(tools.create_output_file_name())

client = TelegramClient("eyes-of-god", api_id, api_hash)


async def search_contact(contact):
    if len(contact) < 5 or len(contact) > 32:
        raise Exception("@username must be from 5 to 32 symbols long")

    global currently_searched_contact
    currently_searched_contact = contact

    print("👁 👁", "Searching:", contact)
    await client.send_message(EyeGodsBot, str("/tg " + currently_searched_contact))


async def repeat_search():
    try:
        global currently_searched_contact
        await search_contact(currently_searched_contact)
    except Exception as e:
        raise e


async def search_next_contact():
    global contacts_to_search
    try:
        # disconnect when all responses are received and no contacts_to_search left to search
        if len(contacts_to_search) == 0:
            print("\nDone. Results are in: ", abs_path_to_output_file)
            await client.disconnect()
        else:
            await search_contact(contacts_to_search.pop())
    except Exception as e:
        raise e


async def start_search():
    global contacts_to_search
    contacts_to_search = []

    try:
        with open(abs_path_to_input_file, "r") as file:
            contacts_to_search = file.readlines()
            if len(contacts_to_search) == 0:
                raise Exception(
                    "input.txt file is either empty or doesn't exist.")
            # else: worksheet.set_column('A:A', contacts_to_search)
    except Exception as e:
        raise e

    await search_next_contact()

current_cell_to_write = 0
def write_to_output_file(phone):
    global current_cell_to_write
    try:
        worksheet.write(current_cell_to_write, 0, "+" + phone + "\n")
        current_cell_to_write += 1
    except Exception as e:
        raise e


@client.on(events.NewMessage(from_users=EyeGodsBot))
@client.on(events.MessageEdited(from_users=EyeGodsBot))
async def handler(event):
    msg = event.message.message
    print(msg)

    try:
        phone = re.search(r"7\d{10}", msg)
        if phone:
            write_to_output_file(phone.group())
            await search_next_contact()
        elif 'Telegram' in msg:
            await search_next_contact()
        elif "Данный логин не принадлежит пользователю." in msg:
            await search_next_contact()
        elif "Вы слишком часто выполняете это действие." in msg:
            delay = re.search(r"Повторите через (\d)", msg)
            await asyncio.sleep(int(delay.group(1)) + 1)
            await repeat_search()
    except Exception as e:
        raise e


async def main():
    global worksheet, workbook
    try:
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(abs_path_to_output_file)
        worksheet = workbook.add_worksheet()

        await client.start()
        await start_search()
        await client.run_until_disconnected()
    except Exception as e:
        await client.disconnect()
        print("Error:", str(e))
        print("Something went wrong 😱😱 Okey, don't panic, just try one more time and hope this message dissapears")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        print("\n Started searching 🔦 \n")
        print("Press Ctrl+C to stop the script, if needed \n")
        loop.run_until_complete(main())
    except (Exception, KeyboardInterrupt) as e:
        print("\n Script has been stopped manually")
    finally:
        workbook.close()
