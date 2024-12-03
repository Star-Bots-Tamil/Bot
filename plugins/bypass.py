from asyncio import create_task, gather
from pyrogram import Client, filters, enums
from pyrogram.filters import command, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.enums import MessageEntityType
from pyrogram.errors import QueryIdInvalid
import os, re
from plugins.core.bypass_checker import direct_link_checker, direct_link_checker1, direct_link_checker2, is_excep_link, process_link_and_send, process_link_and_send1
from plugins.core.bot_utils import convert_time, BypassFilter, BypassFilter1, BypassFilter2
from time import time

# Configs
id_pattern = re.compile(r'^.\d+$') 
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMINS', '1391556668 1242556540').split()]
AUTO_BYPASS = bool(os.getenv("AUTO_BYPASS", "False") == "True")
CHAT_ID = int(os.environ.get("CHAT_ID", -1001542301808))

# Main bypass handler function
@Client.on_message(BypassFilter & (filters.user(ADMINS)))
async def bypass_check(client, message):
    uid = message.from_user.id
    if (reply_to := message.reply_to_message) and (reply_to.text or reply_to.caption):
        txt = reply_to.text or reply_to.caption
        entities = reply_to.entities or reply_to.caption_entities
    elif AUTO_BYPASS or len(message.text.split()) > 1:
        txt = message.text
        entities = message.entities
    else:
        return await message.reply("<b>No Link Provided!</b>")
    wait_msg = await message.reply("<b>Bypassing...</b>")
    start = time()
    links = []
    tasks = []
    for entity in entities:
        if entity.type in (MessageEntityType.URL, MessageEntityType.TEXT_LINK):
            link = txt[entity.offset : entity.offset + entity.length]
            links.append(link)
            tasks.append(create_task(direct_link_checker(link)))
    results = await gather(*tasks, return_exceptions=True)
    output = []
    max_length = 4096
    current_part = ""
    parts = []
    for result, link in zip(results, links):
        if isinstance(result, Exception):
            entry = f"┖ <b>Error:</b> {result}"
        else:
            entry = f"┖ <b>Bypass Link:</b> {result}"
        if len(current_part) + len(entry) > max_length:
            parts.append(current_part.strip())
            current_part = entry
        else:
            current_part += "\n" + entry
    if current_part.strip():
        parts.append(current_part.strip())
    elapsed = time() - start
    footer = (
        f"\n\n<b>Total Links: {len(links)}</b>\n"
        f"<b>Time: {convert_time(elapsed)}</b>\n"
        f"Bypassed By: <a href=https://t.me/TamilMV_Scrapper_Bot><b>1TamilMV Scrapper Bot</b></a>"
    )
    if parts and len(parts[-1]) + len(footer) <= max_length:
        parts[-1] += footer
    else:
        parts.append(footer)
    await wait_msg.delete()
    for part in parts:
        if part.strip():
            await message.reply(part, parse_mode=enums.ParseMode.HTML)

@Client.on_message(BypassFilter1 & filters.user(ADMINS))
async def bypass_check_for_torrent(client, message):
    try:
        # Check if the message is a reply and has text or caption
        if (reply_to := message.reply_to_message) and (reply_to.text or reply_to.caption):
            txt = reply_to.text or reply_to.caption
            entities = reply_to.entities or reply_to.caption_entities
        # Check if the message contains a URL or more than one word
        elif AUTO_BYPASS or len(message.text.split()) > 1:
            txt = message.text
            entities = message.entities
        else:
            return  # No links provided, silently exit

        links = []
        tasks = []

        # Extract URLs from the message
        for entity in entities:
            if entity.type in (MessageEntityType.URL, MessageEntityType.TEXT_LINK):
                link = txt[entity.offset: entity.offset + entity.length]
                links.append(link)
                tasks.append(create_task(process_link_and_send(client, link)))

        # Await all tasks for link processing
        await gather(*tasks, return_exceptions=True)

        await message.reply("<b>Torrent Links Sent Successfully!</b>")

    except Exception as e:
        # Log the error with the exception message
        print(f"Error processing message: {e}")
        await message.reply(f"<b>Error occurred while processing the torrent links:</b> {e}")
        
@Client.on_message(BypassFilter2 & filters.user(ADMINS))
async def bypass_check_for_magnets(client, message):
    try:
        # Check if the message is a reply and has text or caption
        if (reply_to := message.reply_to_message) and (reply_to.text or reply_to.caption):
            txt = reply_to.text or reply_to.caption
            entities = reply_to.entities or reply_to.caption_entities
        # Check if the message contains a URL or more than one word
        elif AUTO_BYPASS or len(message.text.split()) > 1:
            txt = message.text
            entities = message.entities
        else:
            return  # No links provided, silently exit

        links = []
        tasks = []

        # Extract URLs from the message
        for entity in entities:
            if entity.type in (MessageEntityType.URL, MessageEntityType.TEXT_LINK):
                link = txt[entity.offset: entity.offset + entity.length]
                links.append(link)
                tasks.append(create_task(process_link_and_send1(client, link)))

        # Await all tasks for link processing
        await gather(*tasks, return_exceptions=True)

        await message.reply("<b>Torrent Links Sent Successfully!</b>")

    except Exception as e:
        # Log the error with the exception message
        print(f"Error processing message: {e}")
        await message.reply(f"<b>Error occurred while processing the torrent links:</b> {e}")

# Inline query for bypass
@Client.on_inline_query()
async def inline_query(client, query):
    text = query.query.strip()
    if text.startswith("!bp "):
        link = text[4:]
        start = time()
        try:
            result = await direct_link_checker(link, True)
            elapsed = time() - start
            response = f"┎ <b>Source Link:</b> {link}\n┖ <b>Bypass Link:</b> {result}\n\n<b>Time: {convert_time(elapsed)}</b>"
        except Exception as e:
            response = f"<b>Error:</b> {e}"

        answer = InlineQueryResultArticle(
            title="Bypass Result",
            input_message_content=InputTextMessageContent(response, disable_web_page_preview=True),
            description=f"Bypass link: {link}",
        )
        await query.answer(results=[answer], cache_time=0)
    else:
        help_text = """<b><i>1TamilMV Scrapper Bot</i></b>
        
<b>Use the inline query format: !bp [link]</b>
"""
        answer = InlineQueryResultArticle(
            title="Bypass Help",
            input_message_content=InputTextMessageContent(help_text),
        )
        await query.answer(results=[answer], cache_time=0)
