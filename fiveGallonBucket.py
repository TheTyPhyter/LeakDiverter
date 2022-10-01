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

url = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.onion'

os.startfile('<PATH TO tor.exe>')

def sessionHandler(site):
    session = requests.session()
    session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
    r = session.get(site)
    return r


def scraper(page):
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    links = soup.find_all("a")
    filePath = page.url.split('departments/')[-1].replace('%20', ' ')
    for link in links:
        try:
            if link.text.endswith('/'):
                if not os.path.exists(filePath + link.text):
                    print('Making new directory: ', filePath + link.text)
                    os.mkdir(filePath + link.text)
                #print('a', link.text)
                nextdir = sessionHandler(page.url + link.text)
                scraper(nextdir)
            else:
                #print('b', link.text)
                if not os.path.exists(filePath + link.text):
                    print('Saving new file')
                    downloadPage(page.url + link.text, filePath)
                else:
                    print('The file ', "\'\'", filePath + link.text, "\'\'", ' already exists, moving on...')
        except requests.exceptions.ConnectionError:
            print('Error retrieving ', link.text, '. Trying again...')
            scraper(sessionHandler(page.url + link.text))

        except http.client.RemoteDisconnected:
            print('Server ended the session, retrying...')
            scraper(sessionHandler(page.url + link.text))


def downloadPage(file, path):
    outFile = file.split('/')[-1]
    #print('c', outFile)
    with sessionHandler(file) as r:
        #print('d', path)
        with open(path + outFile, 'wb') as f:
            f.write(r.content)
            f.close()


scraper(sessionHandler(url))

