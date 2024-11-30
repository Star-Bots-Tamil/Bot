from pyrogram import Client, __version__
import re, os, time
from datetime import datetime
from pytz import timezone
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server

id_pattern = re.compile(r'^.\d+$')

BOT_TOKEN = os.environ.get("TOKEN", "6043919342:AAGVl9ktA1YDKYvVKu-6xycVX7-9Fg69ZbU")
API_ID = int(os.environ.get("API_ID", 11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
BOT_UPTIME = time.time()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668').split()]

# User string session for `user_client`
USER_STRING_SESSION = os.environ.get("USER_STRING_SESSION", "BQGC3RAANsUaEkcicYxlinT7b-sZqSEmmB3k0U5ejPI11DfFNZWgw95JzOZzClAtOggpEERj6Uw7_Vc4QfYaOZEm9YovvszyJzdZOyrkhgYbE2W4LhtoGkIxh184OswP_atDNQIXEDPzV_8mYtc-9JlilUumlfIDpd-YwSRWYPefy2Yvdvs00q7b5UuMPlVG_psmZWr7Plwp2Z3jscZ6ZoltifWu4MbIvODdxvMMTOjRUNOLHgnlGxanFAiBQn0vD7e8rceLlGWXZ9nKvlQitBvIB4vbUBOIiAglexGoRJZxG0z1dSSBdRiO5jp7QG0vOiNcT-Y7JNaNi2MxwTWIjK6za76X7AAAAABS8Xg8AA")

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="GTStarBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
        )
        # Initialize user_client
        self.user_client = Client(
            "user_client",
            session_string=USER_STRING_SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
        )

    async def start(self):
        # Start the bot client
        await super().start()
        # Start the user client
        await self.user_client.start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = BOT_UPTIME          
        print(f"{me.first_name} is Started...✨️\nMade By :- https://t.me/Star_Bots_Tamil")
        if WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8080).start()
        for id in ADMIN:
            try:
                await self.send_message(id, f"**__{me.first_name} is Started...✨️\nMade By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)__**")                                
            except: 
                pass
        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(LOG_CHANNEL, f"**__{me.mention} is Restarted. !!**\n\n📅 Date :- `{date}`\n⏰ Time :- `{time}`\n🌐 TimeZone :- `Asia/Kolkata`\n\n🉐 Version :- `v{__version__} (Layer {layer})`</b>")                                
            except:
                print("Please Make This Bot Admin in Your Log Channel")

    async def stop(self, *args):
        # Stop the user client
        await self.user_client.stop()
        # Stop the bot client
        await super().stop()
        print("Bot Stopped... Bye")


Bot().run()
