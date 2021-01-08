# Eyes of god 👁👁

“Eyes of god” is an information lookup python script.
You provide tlg nickname and get more information on this nickname if any is available.

This program is based on @EyeGodsBot telegram bot and is an intermediary between user and @EyeGodsBot.

## License

Reading this file means you have accepted the LICENSE.
LICENSE is available near this file, at the same folder.

![eyes of god script](https://github.com/di-sukharev/eyes-of-god/blob/main/img/logo.png)

## Pre-installation of used phone number (skip if you know nothing about it)

1. Login to your [Telegram account](https://my.telegram.org/auth) with the phone number of the developer account to use.
2. Click under API Development tools.
3. A “Create new application” window will appear. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and Short name) can currently be changed later.
4. Click on Create application at the end.

### Important 👋

Remember that your API hash is secret and Telegram won’t let you revoke it. Don’t post it anywhere!

## Installation

1. Install latest python from https://www.python.org/downloads/
2. Open terminal (terminal or console is that black hacker's window where you write commands)
3. Run command `python3 -m pip install dotenv telethon XlsxWriter` (this will install dependencies which are used in the script)

## How to use

1. Add telegram nicknames to search for in `/src/input.txt` file (start nicknames with '@' symbol, every nickname should start with a new line, you can also search by 'telegram id')
2. Open terminal in `eyes-of-god/src` folder (ATTENTION! you must open terminal exactly in `eyes-of-god/src` folder, to check where you are run command `pwd`)
3. Run `python3 main.py` to run the script
4. Provide **used phone number**, **TLG_API_ID** and **TLG_API_HASH** which were created at pre-installation step
5. See search results in `src/output.xlsx` file

## Any questions

For more information go to https://docs.telethon.dev/en/latest/basic/installation.html

### Something more

Use this code with wisdom and always remember that “With great power comes great responsibility.” © Ben Parker, uncle of Peter Parker who is the spider man. Yeah.. Be carefull.
