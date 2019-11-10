#!/usr/bin/env python

import requests
import pandas as pd
import string
import datetime
from time import mktime
import json
# import urllib2
from urllib.request import urlopen
from bs4 import BeautifulSoup

# This is capable of logging into the main page of the website. 
# html = urlopen("http://192.168.1.10:3001/login.html?password=ELOGAdmin/").read()

# queryHeaders = {
    
#     'Host': '192.168.1.10:3001',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate',
#     'Connection': 'keep-alive',
#     'Referer': 'http://192.168.1.10:3001/',
#     'Upgrade-Insecure-Requests': '1'
# }

# url = "http://192.168.1.10:3001/login.html?password=ELOGAdmin"
# r = requests.get(url, data=queryHeaders)

# print(r.content)








# https://www.geeksforgeeks.org/downloading-files-web-using-python/
# fileUrl = 'http://192.168.1.10:3001/start_download.html'
# fileUrl = 'http://192.168.1.10:3001/C1712103-2019-11-09-15-00-00.csv'

# r = requests.get(fileUrl)

csvHeaders = {
    'Host': '192.168.1.10:3001',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'http://192.168.1.10:3001/download_logged_data.html',
    'Upgrade-Insecure-Requests': '1'
}

fileUrl = 'http://192.168.1.10:3001/download_logged_data.html'

r = requests.get(fileUrl, stream=True, data=csvHeaders)

with open('HomeLoggerDataTestDownload.csv', 'wb') as csv:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            csv.write(chunk)









# Beautiful soup finding
# I need to get the date and time for the csv file, also the link to the button. This will then be clicked and put as a url request.

# soup = bs4.BeautifulSoup(r.text, 'lxml')
# buttonLink = soup.find_all('div', id='')

# payload = {field['name']:field['value'] for field in soup.select('form[name="histcsv"] input')}
# csv = requests.post('http://www.ariva.de/quote/historic/historic.csv', data=payload)




# Getting the get request is the first thing, then try and use that to download.
# https://stackoverflow.com/questions/42113041/perform-download-via-download-button-in-python


# Structure of URL of download: http://192.168.1.10:3001/C1712103-2019-11-05-06-35-37.csv

# Request headers: 

# GET /start_download.html HTTP/1.1
# Host: 192.168.1.10:3001
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: keep-alive
# Referer: http://192.168.1.10:3001/download_logged_data.html
# Upgrade-Insecure-Requests: 1

# Response headers: 
# HTTP/1.0 200 OK
# Server: C1712103
# Content-Type: text/html
# Access-Control-Allow-Origin: *
# Content-Length: 1964
# Connection: close

# <HTML><HEAD><meta http-equiv="refresh" content="1;url=C1712103-2019-11-09-14-13-23.csv">
# <TITLE>Elitepro C1712103</TITLE>
# <STYLE TYPE="text/css">
# html
#  {
#   background-image: -ms-linear-gradient(bottom, #FFFFFF 0%, #b0c4de 100%);
#   background-image: -webkit-linear-gradient(bottom, #FFFFFF 0%, #b0c4de 100%);
#   background-image: linear-gradient(bottom, #FFFFFF 0%, #b0c4de 100%);
#  }
# ul#navlist
# {
# margin-left: 0;
# padding-left: 0;
# white-space: nowrap;
# }
# #navlist li
# {
# display: inline;
# list-style-type: none;
# }
# #navlist a { border: 2px solid #a1a1a1; }
# #navlist a { padding: 3px 10px; }
# #navlist a { border-radius: 25px; }
# #navlist a:link, #navlist a:visited
# {
# color: #fff;
# background-color: #036;
# text-decoration: none;
# }
# #navlist a:hover
# {
# color: #fff;
# background-color: #369;
# text-decoration: none;
# }
# </STYLE>
# <script type="text/javascript">
# function load_page(url)
# {
# window.location.assign(url)
# }
# var download_time=134922;
# function start_download_counter()
# {
# document.getElementById('countdown_text').innerHTML="Approximate time remaining: "+download_time+" seconds";
# t = setTimeout('start_download_counter()',1000);
# if(download_time) download_time = download_time-1; else load_page('index.html');
# }
# </script>
# </HEAD>
# <BODY>
# <h1>
#  Elitepro C1712103 Download STARTED
# </h1>
# <div id="navcontainer">
# <ul id="navlist">
# <li id="active"><a href="realtime_values.html" id="current">Realtime Values</a></li>
# <li><a href="view_logged_data.html">View Logged Data</a></li>
# <li><a href="download_logged_data.html">Download Logged Data</a></li>
# <li><a href="logger_settings.html">Logger Settings</a></li>
# <li><a href="logger_properties.html">Logger Properties</a></li>
# <li><a href="logout.html">Log Out</a></li>
# </ul>
# </div>

# Response:
# <PRE><strong>
# DO NOT click away from this page until the download has ENDED.
# <div id="countdown_text"></div>
# </strong></PRE>
# <body onload="start_download_counter()"></BODY></HTML>



# GET /favicon.ico HTTP/1.1
# Host: 192.168.1.10:3001
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
# Accept: image/webp,*/*
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Connection: keep-alive