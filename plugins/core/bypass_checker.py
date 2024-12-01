from re import match
from urllib.parse import urlparse
from plugins.core.exceptions import DDLException
from plugins.scraper import *
import os
from pyrogram import Client

API_ID = int(os.environ.get("API_ID",11973721))
API_HASH = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
STRING_SESSION = os.environ.get("STRING_SESSION", "BQGC3RAANsUaEkcicYxlinT7b-sZqSEmmB3k0U5ejPI11DfFNZWgw95JzOZzClAtOggpEERj6Uw7_Vc4QfYaOZEm9YovvszyJzdZOyrkhgYbE2W4LhtoGkIxh184OswP_atDNQIXEDPzV_8mYtc-9JlilUumlfIDpd-YwSRWYPefy2Yvdvs00q7b5UuMPlVG_psmZWr7Plwp2Z3jscZ6ZoltifWu4MbIvODdxvMMTOjRUNOLHgnlGxanFAiBQn0vD7e8rceLlGWXZ9nKvlQitBvIB4vbUBOIiAglexGoRJZxG0z1dSSBdRiO5jp7QG0vOiNcT-Y7JNaNi2MxwTWIjK6za76X7AAAAABS8Xg8AA")
CHAT_ID = int(os.environ.get("CHAT_ID", -1001542301808))

app = Client("starBots", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION, workers=1000, parse_mode=enums.ParseMode.HTML, no_updates=True)

def is_excep_link(url):
    return bool(
        match(
            r"https?:\/\/.+\.(1tamilmv|gdtot|filepress|pressbee|gdflix|sharespark)\.\S+|https?:\/\/(sharer|onlystream|hubdrive|katdrive|drivefire|skymovieshd|toonworld4all|kayoanime|cinevood|gdflix|filepress|pressbee|filebee|appdrive)\.\S+",
            url,
        )
    )


async def direct_link_checker(link, onlylink=False):
    domain = urlparse(link).hostname

    # Scraper 
    if bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv(link)
    elif bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv1(link)
        
    # Exceptions
    elif bool(match(r"https?:\/\/.+\.technicalatg\.\S+", link)):
        raise DDLException("<b>Bypass Not Allowed !</b>")
    else:
        raise DDLException(
            f"<b>No Bypass Function Found for your Link :</b> <code>{link}</code>"
        )

    if onlylink:
        return blink

    links = []
    while True:
        try:
            links.append(blink)
            blink = await direct_link_checker(blink, onlylink=True)
            if is_excep_link(links[-1]):
                links.append("\n\n" + blink)
                break
  
        except Exception:
            break
    return links

async def process_link_and_send(client, link):
    """
    Processes a link using `direct_link_checker1` and sends each torrent link to the group/channel.
    """
    try:
        torrent_links = await direct_link_checker1(link)
        for torrent_link in torrent_links:
            # Send each torrent link as a separate message
            await app.send_message(CHAT_ID, f"/qbleech {torrent_link}")
    except Exception as e:
        print(f"Error processing {link}: {e}")  # Log the error for debugging


async def direct_link_checker1(link):
    """
    Processes a link and extracts torrent links using `tamilmv1`.
    """
    if bool(match(r"https?:\/\/.+\.1tamilmv\.\S+", link)):
        return await tamilmv1(link)
    else:
        raise DDLException(
            f"<b>No Bypass Function Found for your Link:</b> <code>{link}</code>"
        )
