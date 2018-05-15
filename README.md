# chan-scraper
A scraper made in Python that is capable of downloading any pic-related from any chan or website.

## How to use
Download chan-scraper.py to any location of your liking, then start it through a terminal by using "python chan-scraper.py" (if you use it frequently, you might want to set an alias for this).

## How does it work
chan-scraper.py searches any provided URL for <a>-tags that point to media files (i.e. .png, .jpg, etc.) and starts downloading them. It creates a directory structure in your home folder by default (~/chanscraper) to store your downloads in.

## What sites are supported
Currently it works just fine on 4chan. It also sort-of works on other chans (i.e. ~~Ylilauta~~*, Kohlchan, Ernstchan, 8chan, etc.) but due to files using non-ascii characters it might stop downloading mid-process.

* Ylilauta seems to require JS and/or cookies...
