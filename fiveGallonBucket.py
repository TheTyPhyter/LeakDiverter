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
avoidURLs = ["?C=N;O=D", "?C=D;O=A", "?C=S;O=A", "?C=M;O=A", "Parent Directory"]

os.startfile('<PATH TO tor.exe>')

def sessionHandler(site):
    session = requests.session()
    session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
    r = session.get(site)
    return r


def scraper(page):
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
    links = soup.find_all("a")
    for link in links:
        if link['href'] not in avoidURLs and link.text not in avoidURLs:
            filePath = page.url.split(url)[-1].replace('%20', ' ')
            fullFilePath = filePath + link.text
            fUrl = page.url + link.text
            try:
                if link.text.endswith('/'):
                    if not os.path.exists(fullFilePath):
                        print('Making new directory: ', fullFilePath)
                        os.mkdir(fullFilePath)
                    # print('a', link.text)
                    nextdir = sessionHandler(fUrl)
                    scraper(nextdir)
                else:
                    #print('b', link.text)
                    if not os.path.exists(fullFilePath):
                        print('Saving new file')
                        downloadPage(fUrl, fullFilePath)
                    else:
                        print('The file \'\'', fullFilePath, '\'\' already exists, moving on...')
            except requests.exceptions.ConnectionError:
                print('Error retrieving ', link.text, '. Trying again...')
                scraper(sessionHandler(fUrl))

            except http.client.RemoteDisconnected:
                print('Server ended the session, retrying...')
                scraper(sessionHandler(fUrl))


def downloadPage(url, file):
    with sessionHandler(url) as r:
        #print('d', path)
        with open(file, 'wb') as f:
            f.write(r.content)
            f.close()


scraper(sessionHandler(url))
