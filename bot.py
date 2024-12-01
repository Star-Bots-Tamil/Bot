from pyrogram import Client, __version__, idle
import asyncio
import re, os, time
from pyrogram.raw.all import layer
import pyromod
import pyrogram.utils
from plugins.core.bypass_checker import app as Client2

pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

# Configuration
id_pattern = re.compile(r"^.\d+$")

BOT_TOKEN = os.environ.get("TOKEN", "7713324413:AAGYzSbK5Z9KbhaJGiQdA7Rs-YaYLk4fNiU")
API_ID = int(os.environ.get("API_ID", 11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '1391556668 1242556540').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "BQC2tFkAkYZ0vGtInJ-rss-wOyNAoPYUF1W0G_nZyrjJnG6CGFR645YKCIU2qRAVKWjomO8Gc4VOxIJYMZLBM9z0xoqeZ02w7T4lPWHHbOzstdycyhnSC2Q4iM7QzNuoXOCcN1wGVpLjknPinznoJ7KuAzsprVaMnKpVKdAHkQcxhT9Smtg0T0BCQM41QbLuZCMKOdrRZLodflAXpcm029Fu-N90nhVjlaZCpNrdxQlCBi3deUT0joWn7tTGnHCc_qsFA3QZBqbqCzZgHZbK-xLNv2mzCZtB0M7-Vo-yfrXOXVdUnOKZDgLm0hBY2AN5ESHTJaxPx86FpwuHqnMJgfd8RPTuUAAAAABS8Xg8AA")

bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

user = ''
if len(STRING_SESSION) != 0:
    print("Creating client from USER_SESSION_STRING")
    try:
        user = wztgClient('user', API_ID, API_HASH, session_string=STRING_SESSION,
                        parse_mode=enums.ParseMode.HTML, no_updates=True).start()
    except Exception as e:
        print(f"Failed making client from USER_SESSION_STRING : {e}")
        user = ''

if STRING_SESSION:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()
