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
from telethon.errors import FloodWaitError

load_dotenv()

EyeGodsBot = "EyeGodsBot"

API_ID = "TLG_API_ID"
API_HASH = "TLG_API_HASH"

api_id = tools.get_or_create_dotenv_var(API_ID)
api_hash = tools.get_or_create_dotenv_var(API_HASH)

abs_path_to_input_file = tools.create_abs_path("input.txt")
abs_path_to_output_file = tools.create_abs_path(
    tools.create_output_file_name())

client = TelegramClient("eyes-of-god", api_id, api_hash)


already_searched_times = 0
async def search_contact(contact):
    if len(contact) < 5 or len(contact) > 32:
        raise Exception("@username length must be from 5 to 32 symbols")

    global currently_searched_contact, already_searched_times
    currently_searched_contact = contact
    already_searched_times += 1

    print("\n", "👁 👁", "Searching:", contact)
    await client.send_message(EyeGodsBot, str("/tg " + currently_searched_contact))


already_searhing = False # only one search can be dalayed per moment
async def search_contact_with_delay(contact, delay = 3):
    global already_searhing

    if not already_searhing:
        already_searhing = True

        if delay > 0:
            await asyncio.sleep(delay)
    
        already_searhing = False
        await search_contact(contact)


async def repeat_search_with_delay(timeout = 0):
    global currently_searched_contact
    try:
        await search_contact_with_delay(currently_searched_contact, timeout)
    except Exception as e:
        raise e


async def search_next_contact_with_delay(timeout = 3):
    global search_contacts_list
    try:
        # disconnect when all responses are received and no search_contacts_list left to search
        if len(search_contacts_list) == 0:
            print("\n🕵🏿‍♂️ Done. Results are in: ", abs_path_to_output_file)
            await client.disconnect()
        else:
            await search_contact_with_delay(search_contacts_list.pop(), timeout)
    except Exception as e:
        raise e


async def start_search():
    global search_contacts_list
    search_contacts_list = []

    try:
        with open(abs_path_to_input_file, "r") as file:
            search_contacts_list = file.read().splitlines()
            if len(search_contacts_list) == 0:
                raise Exception(
                    "input.txt file is either empty or doesn't exist.")
    except Exception as e:
        raise e

    await search_next_contact_with_delay(0)


current_xlsx_write_cell = 0
def write_to_output_file(phone):
    global current_xlsx_write_cell
    try:
        worksheet.write(current_xlsx_write_cell, 0, "+" + phone + "\n")
        worksheet.write(current_xlsx_write_cell, 1, currently_searched_contact)
        current_xlsx_write_cell += 1
    except Exception as e:
        raise e


@client.on(events.NewMessage(from_users=EyeGodsBot))
@client.on(events.MessageEdited(from_users=EyeGodsBot))
async def handler(event):
    global currently_searched_contact, already_searched_times

    msg = event.message.message
    print(msg)

    try:
        phone = re.search(r"7\d{10}", msg)

        if phone:
            write_to_output_file(phone.group())
            await search_next_contact_with_delay()

        elif "Анализируем входящие данные..." in msg:
            # saving global vars to local vars
            contact = currently_searched_contact
            time = already_searched_times

            await asyncio.sleep(20)

            # if global vars are the same as local vars after the sleep
            # this means that nothing have happened, so we need to repeat_search()
            still_waiting_for_analyzing = \
                contact == currently_searched_contact and \
                time == already_searched_times

            if still_waiting_for_analyzing:
                await repeat_search_with_delay(0)

        elif "Вы слишком часто выполняете это действие." in msg:
            wait_for = re.search(r"Повторите через (\d)", msg)
            await repeat_search_with_delay(int(wait_for.group(1)) + 1)

        else:
            await search_next_contact_with_delay()

    except Exception as e:
        print("Error in handler:", e)


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
    except FloodWaitError as e:
        print('Flood waited for', e.seconds)
    except (Exception, KeyboardInterrupt) as e:
        print("\n Script has been stopped manually", e)
    finally:
        workbook.close()
