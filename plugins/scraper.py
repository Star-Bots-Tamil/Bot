from cloudscraper import create_scraper
from re import sub
from bs4 import BeautifulSoup

async def tamilmv(url):
    cget = create_scraper().request
    resp = cget("GET", url)
    soup = BeautifulSoup(resp.text, "html.parser")
    mag = soup.select('a[href^="magnet:?xt=urn:btih:"]')
    tor = soup.select('a[data-fileext="torrent"]')
    parse_data = f"<b><u>{soup.title.string}</u></b>"

    for no, (t, m) in enumerate(zip(tor, mag), start=1):
        filename = sub(r"www\S+|\- |\.torrent", "", t.string)
        parse_data += f"""
<b>{no}.</b><code>{filename}</code>
<b>┖ Links : <a href="https://t.me/share/url?url={m['href']}">Magnet 🧲</a> | <a href="{t['href']}">Torrent 🌐</b></a>"""

    max_length = 4096  # Telegram message limit
    if len(parse_data) > max_length:
        parts = [parse_data[i:i + max_length] for i in range(0, len(parse_data), max_length)]
        return parts
    else:
        return [parse_data]
    
async def tamilmv1(url):
    cget = create_scraper().request
    resp = cget("GET", url)
    soup = BeautifulSoup(resp.text, "html.parser")
    tor = soup.select('a[data-fileext="torrent"]')

    torrent_links = []  # List to store filenames and torrent links

    for t in tor:
        filename = sub(r"www\S+|\- |\.torrent", "", t.string)  # Clean the filename
        torrent_link = t['href']
        torrent_links.append({"link": torrent_link, "filename": filename})  # Append as a dictionary
    
    return torrent_links

async def tamilmv2(url):
    cget = create_scraper().request
    resp = cget("GET", url)
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Extract full magnet links
    mag = [m['href'] for m in soup.select('a[href^="magnet:?xt=urn:btih:"]')]
    
    # List to store parsed data
    parsed_list = []

    # Generate parsed list
    for m in mag:
        filename = sub(r"www\S+|\- |\.torrent", "", m.split('&dn=')[1] if '&dn=' in m else "Unknown")  # Extract filename from magnet link or use 'Unknown'
        parsed_list.append({"magnet": m, "filename": filename})
    
    # Return only the parsed list
    return parsed_list
        
