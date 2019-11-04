#!/usr/bin/env python

import requests
import pandas as pd
import string
import datetime
from time import mktime
import json
# import urllib2
from urllib.request import urlopen

html = urlopen("http://192.168.1.10:3001/login.html?password=ELOGAdmin/").read()


# https://www.geeksforgeeks.org/downloading-files-web-using-python/
# fileUrl = 'http://192.168.1.10:3001/start_download.html'

# r = requests.get(fileUrl, stream=True)

# with open('HomeLoggerDataTestDownload.csv', 'wb') as csv:
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk:
#             csv.write(chunk)





