from pyrogram import Client, __version__, idle
import asyncio
import re, os, time
from datetime import datetime
from pytz import timezone
from pyrogram.raw.all import layer
from aiohttp import web
from route import web_server
from plugins.core.bypass_checker import app as Client2

# Configuration
id_pattern = re.compile(r"^.\d+$")

BOT_TOKEN = os.environ.get("TOKEN", "7713324413:AAGYzSbK5Z9KbhaJGiQdA7Rs-YaYLk4fNiU")
API_ID = int(os.environ.get("API_ID", 11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
BOT_UPTIME = time.time()
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))
WEBHOOK = bool(os.environ.get("WEBHOOK", True))
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668 1242556540').split()]
STRING_SESSION = os.environ.get("STRING_SESSION", "BQGC3RAANsUaEkcicYxlinT7b-sZqSEmmB3k0U5ejPI11DfFNZWgw95JzOZzClAtOggpEERj6Uw7_Vc4QfYaOZEm9YovvszyJzdZOyrkhgYbE2W4LhtoGkIxh184OswP_atDNQIXEDPzV_8mYtc-9JlilUumlfIDpd-YwSRWYPefy2Yvdvs00q7b5UuMPlVG_psmZWr7Plwp2Z3jscZ6ZoltifWu4MbIvODdxvMMTOjRUNOLHgnlGxanFAiBQn0vD7e8rceLlGWXZ9nKvlQitBvIB4vbUBOIiAglexGoRJZxG0z1dSSBdRiO5jp7QG0vOiNcT-Y7JNaNi2MxwTWIjK6za76X7AAAAABS8Xg8AA")

# Bot Class
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
        self.mention = None
        self.username = None
        self.uptime = BOT_UPTIME

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = BOT_UPTIME
        print(f"{me.first_name} is Started...✨️\nMade By :- https://t.me/Star_Bots_Tamil")

        if WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()

        for admin_id in ADMIN:
            try:
                await self.send_message(admin_id, f"**__{me.first_name} is Started...✨️\nMade By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)__**")
            except Exception as e:
                print(f"Failed to send message to admin {admin_id}: {e}")

        if LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                await self.send_message(LOG_CHANNEL, f"**__{me.mention} is Restarted. !!**\n\n📅 Date :- `{date}`\n⏰ Time :- `{time_str}`\n🌐 TimeZone :- `Asia/Kolkata`\n\n🉐 Version :- `v{__version__} (Layer {layer})`</b>")
            except Exception as e:
                print(f"Error sending to log channel: {e}")

    async def stop(self, *args):
        try:
            await super().stop()
            print("Bot Stopped... Bye")
        except Exception as e:
            print(f"Error stopping bot: {e}")


# Start and run bot with async functions
async def start_bots():
    bot = Bot()
    apps = [Client2, bot]

    # Start all applications
    await asyncio.gather(*[app.start() for app in apps])

    # Run the bot
    await bot.start()

    # Run Webhook Server if needed
    if WEBHOOK:
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        await web.TCPSite(app_runner, "0.0.0.0", 8080).start()

    # Keep bot running
    try:
        await bot.idle()
    except Exception as e:
        print(f"Error during bot idle: {e}")
    finally:
        # Stop the bot and apps
        await asyncio.gather(*[app.stop() for app in apps])


# Main entry point to start the bot
if __name__ == "__main__":
    asyncio.run(start_bots())
    
