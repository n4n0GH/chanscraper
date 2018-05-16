#! /usr/bin/python
#
# coding: utf-8

# chan-scraper.py is a standalone mass downloader for any arbitrary
# chan or website in general. It looks for links that point to media
# files and downloads them accordingly.

# TODO: make script compatible with Python 2.7 and Python 3.x
# TODO: have only hrefs in array if the <a> has an <img> child
# TODO: args handling for direct downloading
# TODO: custom download directory
# TODO: check for text-links on URL and paste them into txt-file

# import some libraries
from __future__ import print_function
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import sys
import os

# clear screen and set terminal title
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
sys.stdout.write("\x1b]2;chan scraper\x07")

# print ASCII intro
print("""
      _
     | |
  ___| |__   __ _ _ __    ___  ___ _ __ __ _ _ __   ___ _ __
 / __| '_ \ / _` | '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| (__| | | | (_| | | | | \__ \ (__| | | (_| | |_) |  __/ |
 \___|_| |_|\__,_|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                            | |
  Download pic-related from any chan        |_|       v0.2

""")

# set up UA so *chan accepts the request
ua = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
      'AppleWebKit/537.11 (KHTML, like Gecko)'
      'Chrome/23.0.1271.64 Safari/537.11'}

# get URL from user
if sys.version_info[:2] <= (2, 7):
    user_input = raw_input
else:
    user_input = input

sep = "#"
url = user_input("Input URL to scrape: \n > ").split(sep, 1)[0]

# make some soup
req = urllib2.Request(url, headers=ua)
soup = BeautifulSoup(urllib2.urlopen(req), "lxml")

# split the url into parts
parse = url.split('/')
base = parse[2]
path = parse[3]
thread = parse[-1]

# fetch all files and append to array
scrape = []

for img in soup.select('a[href$=jpg],'
                       'a[href$=jpeg],'
                       'a[href$=png],'
                       'a[href$=gif],'
                       'a[href$=webm]'):
    img_url = urlparse.urljoin(url, img['href']).encode('utf-8')
    if img_url not in scrape:
        scrape.append(img_url)

# set up path names and other variables for downloads
home = os.path.expanduser("~")
fpath = os.path.join(home, "chanscraper", base, path, thread)
s = 0
e = 0
i = 1

# create directory if necessary
if not os.path.exists(fpath):
    os.makedirs(fpath)

# download array to disk
for img in scrape:
    file_name = img.split('/')[-1]
    full_path = os.path.join(fpath, file_name)
    if not os.path.exists(full_path):
        try:
            filedata = urllib2.urlopen(img)
            print("Grabbing [" + str(i) + "/" +
                  str(len(scrape) - s) + "]", end="\r")
            sys.stdout.flush()
            with open(full_path, 'wb') as f:
                f.write(filedata.read())
            i += 1
        except urllib2.HTTPError:
            e += 1
            print("HTTP error, skipping [" + str(e) + "]")
    else:
        s += 1
        print("File already exists, skipping [" +
              str(s) + "]...", end="\r")

print("Downloaded " + str(i - e - s) + " new files!")
