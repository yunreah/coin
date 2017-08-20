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


coinyen = {}
url = "https://coinmarketcap.com/all/views/all/#JPY"
lineurl = "https://notify-api.line.me/api/notify"
token = ""
headers = {"Authorization" : "Bearer "+ token}


#web
coinlist = []
target_html = requests.get(url).text
html = lxml.html.fromstring(target_html)
for coin in re.findall('<tr id="id-([A-Z,a-z,0-9]+)"',target_html):
    volume = html.xpath('//*[@id="id-' + coin.lower() + '"]/td[7]/a')[0].text[1:].replace(",","")
    symbol = html.xpath('//*[@id="id-' + coin.lower() + '"]/td[3]')[0].text
    try:
        volume = int(volume)
    except:
        continue
    coinlist.append([coin, volume, symbol])
#    coinlist = [[] for j in range(len(allcoin))]
#exchangerate = float(re.findall('data-jpy="([0-9]+.[0-9]+)', target_html)[0])
coinlist = sorted(coinlist, key=lambda x: x[1],reverse=True)

for coin in coinlist:
    if coin[1] <= 200000:
        break
    url2 =  "https://coinmarketcap.com/currencies/" + coin[0] + "/#markets"
    target_html = requests.get(url2).text
    html = lxml.html.fromstring(target_html)
    pricelist = []

    #market num
    for i  in range(1,100):
        try:
            pair = html.xpath('//*[@id="markets-table"]/tbody/tr[' + str(i) + ']/td[3]/a')[0].text
        except:
            break
        symbol = coin[2] + "/ETH"
        if symbol != pair:
            continue

        #/ETH
        volume24 = float(html.xpath('//*[@id="markets-table"]/tbody/tr[' + str(i) + ']/td[4]/span')[0].text[1:].replace(',',""))
        if volume24 < 10000:
            continue
        volume = float(html.xpath('//*[@id="markets-table"]/tbody/tr[' + str(i) + ']/td[6]')[0].text[:-1])
        source = html.xpath('//*[@id="markets-table"]/tbody/tr[' + str(i) + ']/td[2]/a')[0].text
        price = float(html.xpath('//*[@id="markets-table"]/tbody/tr[' + str(i) + ']/td[5]/span')[0].text[1:])
        pricelist.append([coin[0], source, price, volume])

    if len(pricelist)  < 2:
        continue
    pricelist = sorted(pricelist, key=lambda x: x[2], reverse=True)
    div = pricelist[0][2] / pricelist[-1][2]
    if div >= 1.1:
        message = coin[0] + " " + str(round(div,1)) + " " + pricelist[0][1] +  " " + pricelist[-1][1]
        print message
        payload = {"message": message}
        r = requests.post(lineurl, headers=headers, params=payload)

"""""
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
"""