from cloudscraper import create_scraper
from re import sub
from bs4 import BeautifulSoup

from cloudscraper import create_scraper
from bs4 import BeautifulSoup
from re import sub

async def tamilmv(url):
    cget = create_scraper().request
    resp = cget("GET", url)
    soup = BeautifulSoup(resp.text, "html.parser")
    mag = [m['href'] for m in soup.select('a[href^="magnet:?xt=urn:btih:"]')]
    tor = soup.select('a[data-fileext="torrent"]')
    parse_data = f"<b><u>{soup.title.string}</u></b>"
    for no, (t, m) in enumerate(zip(tor, mag), start=1):
        filename = sub(r"www\S+|\- |\.torrent", "", t.string)
        parse_data += f"""
        
<b>{no}.</b> <code>{filename}</code>
┖ <b>Links :</b> <a href="{m}"><b>Magnet </b>🧲</a>  | <a href="{t['href']}"><b>Torrent 🌐</b></a>"""
    return parse_data
    
async def tamilmv1(url):
    cget = create_scraper().request
    resp = cget("GET", url)
    soup = BeautifulSoup(resp.text, "html.parser")
    tor = soup.select('a[data-fileext="torrent"]')

    torrent_links = []  # List to store filenames and torrent links

    for t in tor:
        filename = re.sub(r"www\S+|\- |\.torrent", "", t.string)  # Clean the filename
        torrent_link = t['href']
        torrent_links.append({"filename": filename, "link": torrent_link})  # Append as a dictionary
    
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
        parsed_list.append({"filename": filename, "magnet": m})
    
    # Return only the parsed list
    return parsed_list
        
