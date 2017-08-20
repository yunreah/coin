# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import urllib,urllib2
import lxml.html
import time, sqlite3
import threading
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.Utils import formatdate

def sleeptime(coin):
    #print coin + "wait"
    time.sleep(3600)
    flaglist[coin] = 0

coinList = ["Bitcoin", "Ethereum","NEM","Litecoin","IOTA","Dash","Lisk","OmiseGo","Civic","Status","TenX","InsureX","Bitland",
            "Ripple","MonaCoin"]
lowalert = {"Bitcoin":360000,"Ethereum":30000,"Litecoin":4200,"NEM":25,"IOTA":60,"Dash":20000,"Lisk":220,
            "OmiseGo":600,"Civic":50,"Status":6,"TenX":400}
hihalert = {"Ethereum":35000,"InsureX":60, "Bitland":70,"NEM":40,"MonaCoin":60}

flaglist = {"Bitcoin":0, "Ethereum":0,"NEM":0,"Litecoin":0,"IOTA":0,"Dash":0,"Lisk":0,"OmiseGo":0,"Civic":0,"Status":0,
            "TenX":0,"InsureX":0,"Bitland":0, "Ripple":0,"MonaCoin":0}

coinyen = {}
url = "https://coinmarketcap.com/all/views/all/#JPY"
lineurl = "https://notify-api.line.me/api/notify"
token = ""
headers = {"Authorization" : "Bearer "+ token}

while (1):
    #web
    target_html = requests.get(url).text
    html = lxml.html.fromstring(target_html)
    exchangerate = float(re.findall('data-jpy="([0-9]+.[0-9]+)', target_html)[0])

    for coin in coinList:
        xpath = '//*[@id="id-' + coin.lower()  + '"]'
        priceUSD = float(html.xpath(xpath + "/td[5]/a")[0].text[1:])
        priceJPY = priceUSD / exchangerate
        coinyen.update({coin: priceJPY})

    print coinyen

    #LINE
    for coin, lowprice in lowalert.items():
        if coinyen[coin] < lowprice:
            message = coin + " is down " + str(coinyen[coin])
            print message
            payload = {"message": message}
            #files = {"imageFile": open("test.jpg", "rb")}
            r = requests.post(lineurl, headers=headers, params=payload)

    for coin, highprice in hihalert.items():
        if coinyen[coin] > highprice and flaglist[coin] == 0:
            message = coin + " is up " + str(coinyen[coin])
            print message
            payload = {"message": message}
            #files = {"imageFile": open("test.jpg", "rb")}
            r = requests.post(lineurl, headers=headers, params=payload)
            flaglist[coin] = 1
            thread1 = threading.Thread(target=sleeptime(coin), name=coin)
            thread1.start()
    time.sleep(300)