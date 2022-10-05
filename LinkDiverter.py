"""
You must have tor browser and be running the tor service to download from .onion urls.
This script will download all files in an open directory.
useful for downloading entire data leaks.
Painfully slow, but it's python and TOR and Im bad at scripting so idk what you expected...
Uncomment print lines for debugging.
"""

import sys
import http
import os.path
import requests
from bs4 import BeautifulSoup

try:
    url = sys.argv[1]
    tor = sys.argv[2]

    avoidURLs = ["?C=N;O=D", "?C=D;O=A", "?C=S;O=A", "?C=M;O=A", "Parent Directory"]

    os.startfile(tor)

    def sessionHandler(site):
        session = requests.session()
        session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
        r = session.get(site)
        return r


    def scraper(page):
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="iso-8859-1")
        links = soup.find_all("a")
        fileCount = 0
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
                            fileCount += 1
                            print(fileCount, 'files downloaded')
                        else:
                            print("The file '", fullFilePath, "' already exists, moving on...'")
                except requests.exceptions.ConnectionError:
                    print('Error retrieving ', link.text, '. Trying again...')
                    os.system("taskkill /f /im tor.exe")
                    os.startfile(tor)
                    scraper(sessionHandler(fUrl))

                except http.client.RemoteDisconnected:
                    print('Server ended the session, retrying...')
                    os.system("taskkill /f /im tor.exe")
                    os.startfile(tor)
                    scraper(sessionHandler(fUrl))


    def downloadPage(url, file):
        print('Downloading: ', file)
        with sessionHandler(url) as r:
            #print('d', path)
            with open(file, 'wb') as f:
                f.write(r.content)
                f.close()
    scraper(sessionHandler(url))

except IndexError:
    print("Welcome to the LeakDiverter.\n Run again with a valid URL [including(especially)] .onion URLs to an"
          " open directory\n"
          "'usage: python3 LeakDiverter.py <valid URL> <path to tor.exe>'")
