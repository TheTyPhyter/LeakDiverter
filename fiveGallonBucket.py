"""
You must have tor browser and be running the tor service to download from .onion urls.
This script will download all files in an open directory.
useful for downloading entire data leaks.
Painfully slow, but it's python and TOR and Im bad at scripting so idk what you expected...
Uncomment print lines for debugging.
"""
import http
import os.path
import requests
from bs4 import BeautifulSoup

url = 'xxxxxxxxxxxxxxxxxxxxxxxxxx.onion'


def sessionHandler(site):
    session = requests.session()
    session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
    r = session.get(site)
    return r


def scraper(page):
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    links = soup.find_all("a")
    for link in links:
        try:
            if link.text.endswith('/'):
                #print('a', link.text)
                nextdir = sessionHandler(page.url + link['href'])
                scraper(nextdir)
            else:
                #print('b', link.text)
                if not os.path.exists(link['href']):
                    print('Saving new file')
                    downloadPage(page.url + link['href'])
                else:
                    print('The file ', link.text, ' already exists, moving on...')
        except requests.exceptions.ConnectionError:
            print('Error retrieving ', link.text, '. Trying again...')
            scraper(sessionHandler(page.url + link.text))

        except http.client.RemoteDisconnected:
            print('Server ended the session, retrying...')
            scraper(sessionHandler(page.url + link.text))


def downloadPage(file):
    outFile = file.split('/')[-1]
    #print('c', outFile)
    with sessionHandler(file) as r:
        with open(outFile, 'wb') as f:
            f.write(r.content)
            f.close()


scraper(sessionHandler(url))
