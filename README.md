# chan-scraper
A scraper made in Python that is capable of downloading any pic-related from any chan or website.

![chan-scraper v0.2](https://github.com/n4n0GH/chan-scraper/blob/master/Screenshot_20180525_094952.png)

## Requirements
- Python 2.7
- bs4
- lxml

## How to use
Download chanscraper.py to any location of your liking, then start it through a terminal by using "python chanscraper.py". I recommend setting up an alias for this in your terminal emulator of choice.

## Arguments
### -h, --help
Invoke help page for the script and read about the available arguments.
### -d (URL), --download (URL)
Specify the URL to download from. Last part of the URL will be used as the directory title to write to. This can be a made-up name and doesn't have to be part of the original URL. When using multiple URLs to download from, each URL has to be seperated by a space.
### -t, --timeout
Change the default connection timeout from 10 seconds to something else. Argument takes integers only.
### -e, --exit
Exit the terminal parent process once the download is complete. Fire and forget.
### -D (DIR), --directory (DIR)
Use a custom directory to write the files to. Default is ~/chanscraper; only absolute paths are allowed. Check your permissions on that directory.
### -c, --cleanup
Starts the duplication finder located in dupe.py and automatically removes duplicates of image files in the current download directory. Supports multi-URL downloads.

## How does it work
chanscraper.py searches any provided URL for <a>-tags that point to media files (i.e. .png, .jpg, etc.) and starts downloading them. It creates a directory structure in your home folder by default (~/chanscraper) to store your downloads in.

## What sites are supported
It works on any imageboard that doesn't block the requests.
