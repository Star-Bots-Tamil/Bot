from pyrogram import Client, __version__, idle
import asyncio
import re, os, time
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server
from plugins.core.bypass_checker import app as Client2

# Configuration
id_pattern = re.compile(r"^.\d+$")

BOT_TOKEN = os.environ.get("TOKEN", "7713324413:AAGYzSbK5Z9KbhaJGiQdA7Rs-YaYLk4fNiU")
API_ID = int(os.environ.get("API_ID", 11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '1391556668 1242556540').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "BQGC3RAANsUaEkcicYxlinT7b-sZqSEmmB3k0U5ejPI11DfFNZWgw95JzOZzClAtOggpEERj6Uw7_Vc4QfYaOZEm9YovvszyJzdZOyrkhgYbE2W4LhtoGkIxh184OswP_atDNQIXEDPzV_8mYtc-9JlilUumlfIDpd-YwSRWYPefy2Yvdvs00q7b5UuMPlVG_psmZWr7Plwp2Z3jscZ6ZoltifWu4MbIvODdxvMMTOjRUNOLHgnlGxanFAiBQn0vD7e8rceLlGWXZ9nKvlQitBvIB4vbUBOIiAglexGoRJZxG0z1dSSBdRiO5jp7QG0vOiNcT-Y7JNaNi2MxwTWIjK6za76X7AAAAABS8Xg8AA")

bot = Client("Renamer", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root='plugins'))

if WEBHOOK:
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", 8080).start()

if STRING_SESSION:
    apps = [Client2,bot]
    for app in apps:
        app.start()
    idle()
    for app in apps:
        app.stop()
    
else:
    bot.run()
