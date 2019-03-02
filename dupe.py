#!/usr/bin/env python
# Recursively find duplicate files.
#
# Author: slowpoke (Proxy) < mail at slowpoke dot io >
# Modified: n4n0 < n4n0 at tuta dot io >
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

from __future__ import print_function
from collections import defaultdict
from datetime import datetime
import argparse
import hashlib
import os
import re


start = datetime.now()


def hash(path):
    '''Hash a file's content.'''
    with open(path, "rb") as file_:
        hash_ = hashlib.sha1(file_.read()).hexdigest()
        return int(hash_, 16)


def crawl(root, *exts):
    '''Recursively search a given path for files matching a list extensions.'''
    # construct the regexp
    regexp = "|".join(["\." + ext + "$" for ext in exts])
    pattern = re.compile(regexp)

    # matches are a dict of sha1sum : [filenames]
    matches = defaultdict(list)

    for item in os.walk(root):
        paths = item[2]
        for path in paths:
            if re.search(pattern, path):
                file_ = item[0] + os.sep + path
                hash_ = hash(file_)
                matches[hash_].append(file_)
    return matches


def format(files):
    counter_ = 0
    '''Niceify the output.'''
    for file_ in files.values():
        # print only if there are actually duplicate files
        if len(file_) > 1:
            print("Keeping " + file_[-1])
            file_.remove(file_[-1])
            for path in file_:
                counter_ += 1
                print("Removing " + path)
                os.remove(path)
    finish = datetime.now() - start
    finish = str(finish.total_seconds())
    print("\033[42m\033[30mDuplicate detection finished in " +
            finish + " seconds!\033[0m")
    print("\033[33mDeleted files: " + str(counter_) + "\033[0m\n")


def main(path):
    print("""                                """, end="\r")
    print("Searching in:\n\033[32m>\033[0m " + path +"\033[0m")
    extensions = ["jpg", "jpeg", "png", "gif"]
    files = crawl(path, *extensions)
    format(files)

if __name__ == "__main__":
    main()
