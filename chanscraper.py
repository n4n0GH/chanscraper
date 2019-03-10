#!/usr/bin/python
#
# coding: utf-8


# chanscraper.py is a standalone mass downloader for any arbitrary
# chan or website in general. It looks for links that point to media
# files and downloads them accordingly.


# TODO: have only hrefs in array if the <a> has an <img> child
# TODO: custom download directory
# TODO: check for text-links on URL and paste them into txt-file
# TODO: circumvent bot detection on websites like ylilauta
# TODO: periodic downloads
# TODO: specify additional filetypes through sysargs
# TODO: use config file to store additional filetypes, custom directories or if
#       script should exit terminal upon completion


# import some libraries
from __future__ import print_function
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import urllib2
import urlparse
import argparse
import subprocess
import sys
import os
import re
import signal
import hashlib
import dupe


# set classes for colors
class fg:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    WHITE = '\033[37m'


class bg:
    GREEN = '\033[42m'


class style:
    BLINK = '\33[5m'
    CLINE = '\x1b[2K'
    RESET_ALL = '\033[0m'


# set up notification modules for different operating systems
def notify(message):
    if sys.platform == "linux":
        subprocess.call(["notify-send", "-i", "document-save",
            "chanscraper", message])
    elif sys.platform == "darwin":
        os.system("""
                osascript -e 'display notification "{}" with title "{}"'
                """.format(message, "chanscraper"))
    elif sys.platform == "win32":
        print("Sorry, no fancy notifications for you.")
    return


# set up argparser
parser = argparse.ArgumentParser(description="""
                                 A standalone mass downloader for any
                                 arbitrary chan or website in general.\n
                                 Will pick any <a>-tags that end in
                                 media files (i.e. jpg, png, mp4) and
                                 write them to disk.
                                 """)
parser.add_argument("-d", "--download",
                    help="start a direct download from a provided URL,\
                    enter multiple URLs with a space to seperate them",
                    nargs="+", metavar="(URL)")
parser.add_argument("-t", "--timeout",
                    help="set a custom timout for downloads in seconds,\
                    default is 10", nargs=1, type=int,
                    metavar="(SECONDS)")
parser.add_argument("-c", "--cleanup",
                    help="removes files with duplicate sha1 digests",
                    action="store_true")
parser.add_argument("-e", "--exit",
                    help="automatically closes terminal after finishing",
                    action="store_true")
parser.add_argument("-D", "--directory",
                    help="set a custom parent directory to write to,\
                    default is your user's home directory; use absolute paths",
                    nargs=1, metavar="(DIR)")
parser.add_argument("-v", "--verbose",
                    help="print additional messages during processing for \
                    debugging purposes", action="store_true")
args = parser.parse_args()


# clear screen and set terminal title
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
sys.stdout.write("\x1b]2;chanscraper\x07")

if args.verbose:
    print(bg.GREEN + fg.BLACK + "VERBOSE MODE ACTIVE" + style.RESET_ALL)

# print ASCII intro
print("""\033[32m
      _
     | |
  ___| |__   __ _ _ __    ___  ___ _ __ __ _ _ __   ___ _ __
 / __| '_ \ / _` | '_ \  / __|/ __| '__/ _` | '_ \ / _ \ '__|
| (__| | | | (_| | | | | \__ \ (__| | | (_| | |_) |  __/ |
 \___|_| |_|\__,_|_| |_| |___/\___|_|  \__,_| .__/ \___|_|
                                            | |
                                            |_|         \033[31mv0.6
\033[0m
""")


# set up UA so *chan accepts the request
ua = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11'}


# set up scraper logic
def logic():
    # start counting time
    start = datetime.now()

    while True:
        # split the url into parts
        parse = url.split('/')
        base = parse[2]
        path = parse[3]
        thread = parse[-1]

        # print debugging
        if args.verbose:
            print("base: " + base)
            print("path: " + path)
            print("thread: " + thread)
            print("url: " + url)

        # circumvent "no JS" detection
        # include logic here

        print(fg.GREEN + "Connecting...", end="\r")
        sys.stdout.flush()

        # make some soup and end on 404
        try:
            req = urllib2.Request(url, headers=ua)
            soup = BeautifulSoup(urllib2.urlopen(req), "lxml")
            if args.verbose:
                print("parsed sourcecode: \n" + str(soup))
        except urllib2.URLError:
            print(fg.RED + "Host unreachable, stopping...\n" + style.RESET_ALL)
            break

        # fetch all files and append to array
        scrape = []
        for img in soup.select('a[href$=jpg],'
                               'a[href$=jpeg],'
                               'a[href$=png],'
                               'a[href$=gif],'
                               'a[href$=webm],'
                               'a[href$=mp4],'
                               'a[href$=mp3]'):
            img_url = urlparse.urljoin(url, img['href']).encode('utf-8')
            if img_url not in scrape:
                scrape.append(img_url)
                if args.verbose:
                    print("found item: " + img_url)

        print(fg.GREEN + "Setting up directory...", end="\r")
        sys.stdout.flush()

        # set up path names and other variables for downloads
        if args.directory:
            home = args.directory[0]
            fpath = os.path.join(home, base, path, thread)
        else:
            home = os.path.expanduser("~")
            fpath = os.path.join(home, "chanscraper", base, path, thread)
        i = e = s = 0

        if args.timeout:
            kill = args.timeout[0]
        else:
            kill = 10

        # create directory if necessary
        if not os.path.exists(fpath):
            os.makedirs(fpath)

        print(style.CLINE + fg.GREEN + "Preparing scraper...", end="\r")
        sys.stdout.flush()

        # download array to disk
        for img in scrape:
            file_name = img.split('/')[-1]
            full_path = os.path.join(fpath, file_name)
            if not os.path.exists(full_path):
                try:
                    filedata = urllib2.urlopen(img, timeout=kill)
                    i += 1
                    print(style.CLINE + fg.GREEN +
                          "Grabbing file... [" + str(i) + "/" +
                          str(len(scrape) - s) + "]", end="\r")
                    with open(full_path, 'wb') as f:
                        f.write(filedata.read())
                    sys.stdout.flush()
                except urllib2.HTTPError:
                    e += 1
                    print(style.CLINE + fg.RED + "HTTP error, skipping... [" +
                          str(e) + "]", end="\r")
                except urllib2.URLError:
                    e += 1
                    print(style.CLINE + fg.RED +
                          "Timeout or bad URL, skipping... [" + str(e) + "]",
                          end="\r")
            else:
                s += 1
                print(fg.YELLOW + "File already exists, skipping... [" +
                      str(s) + "]", end="\r")
                sys.stdout.flush()

        # check passed time and convert to readable string
        finish = datetime.now() - start
        finish = str(finish.total_seconds())

        # print success messages as notification window and in terminal
        if i - e == 0:
            notify("No new files have been downloaded.")
        else:
            notify("Downloaded " + str(i - e) + " new files from /" + path +
               "/ in " + finish + " seconds!")
        print(bg.GREEN + fg.BLACK +
              "Downloaded " + str(i - e) + " new files from /" + path +
              "/ in " + style.BLINK + finish + " seconds!\n" +
              style.RESET_ALL + fg.YELLOW + "Skipped: " + str(s) +
              style.RESET_ALL + " | " + fg.RED + "Errors: " + str(e) +
              style.RESET_ALL + "\n")

        # remove duplicate files if args is set
        if args.cleanup:
            print("Starting duplicate detection...", end="\r")
            dupe.main(fpath)
            break


# get URL from args or user
sep = "#"

if not args.download:
    url = raw_input("Input URL to scrape: \n" + fg.GREEN +
                    "> " + style.RESET_ALL).split(sep, 1)[0]
    logic()
else:
    for address in args.download:
        url = address.split(sep, 1)[0]
        print("Scraping from: \n" + fg.GREEN + "> " + style.RESET_ALL + url)
        logic()


# exit terminal emulator
if args.exit:
    os.kill(os.getppid(), signal.SIGHUP)
