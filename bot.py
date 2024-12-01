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
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '1391556668 1242556540 5239847373').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "1BVtsOKEBu5Pf_Oesjuxt4TIzNijt1iMjJ8hEa3xtURQFrsd0GFYLhS_XFm2iJ61NfFeKR5icfMSu_SWH3eRvvdZ-X7IyOVFZuQ4sHKoiju_WXCH4uQqqd7vB7_9hGyMbDk7mUgjVKNkRg0trupt-5mu8pAeWAZ3US61kBnLKvsMYSjiaiL3uWI3UDfzyNQzFhf_hXWF_XskD0QrMPS87wEd85iNzXBgBE9Sae2haJ8YppGWxhcGtmJDSqHnDSlxh2dFLBZ1K_o7zxE6i1FrOaqEL_gKW87xqc2W43kCsUj-s9A9GyXdP7aUxu1Mku5j3GyMxEWS79Yku7AfxyeGUYhTw5dXGScE=")

bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

if STRING_SESSION:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()
