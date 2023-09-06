"""
           _                _    _____  _                _            
          | |              | |  |  __ \(_)              | |           
          | |     ___  __ _| | _| |  | |___   _____ _ __| |_ ___ _ __ 
          | |    / _ \/ _` | |/ / |  | | \ \ / / _ \ '__| __/ _ \ '__|
          | |___|  __/ (_| |   <| |__| | |\ V /  __/ |  | ||  __/ |   
          |______\___|\__,_|_|\_\_____/|_| \_/ \___|_|   \__\___|_|   
                                                             
.:/>  Python Script for scraping and downloading files from .onion Websites <\:.
              
What:
- This script will download all files in an open directory from a .onion URL.
- Written by TheTyPhyter | Tweaked by UberGuidoZ

Requirements:
- You must have Python 3 installed and working correctly.
- You must have the Tor browser and be running the Tor service.
- You must provide the full path to the Tor EXE and the URL.

Result:
- All files that can be downloaded will be saved to the LDD folder.
  (That folder will be within the directory this script is run from.)
- Painfully slow, but it's Tor and Python so I don't know what you were expecting.

Syntax: python3 LeakDiverter.py <valid URL> full_path_to_Tor.exe

Troubleshooting:
- Read and follow the directions.
- Uncomment print lines for debugging.

"""

import sys
import http
import os.path
import requests
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import unquote

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
                filePath = unquote(page.url.split(url)[-1])
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
                        # print('b', link.text)
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
        # Create the "LDD" directory if it doesn't exist
        if not os.path.exists("LDD"):
            os.mkdir("LDD")
    
        # Combine the "LDD" directory path with the file name
        download_path = os.path.join("LDD", file)
    
        print('Downloading: ', download_path)
        with sessionHandler(url) as r:
            with open(download_path, 'wb') as f:
                f.write(r.content)
                f.close()
    scraper(sessionHandler(url))

except IndexError:
    print   (colored('Welcome to the LeakDiverter.\n\n', 'green'),
             colored('Run again with a valid .onion URL to an open directory\n\n', 'blue'),
             colored("usage: 'python3 LeakDiverter.py <valid URL> <full_path_to_Tor.exe>'\n", 'green'))
