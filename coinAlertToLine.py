# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import lxml.html
import time
import threading
from datetime import datetime
import os
import re

def sleeptime(coin):
    #print coin + "wait"
    time.sleep(waittime * 60)
    flaglist[coin] = 0

############################設定############################################
token = "" #ここにLINEのアクセストークン
cycle = 2 #アラートを送る周期 cycle分毎に価格を確認
waittime = 60 #1度アラートが送信されて，また次に送信されるまでの時間(分)
coinList = ["Bitcoin", "Ethereum","NEM","Litecoin","IOTA","Dash","Lisk","OmiseGo","Civic","Status","TenX","InsureX","Bitland",
            "Ripple","MonaCoin","Stox","NEO","CoinDash","Waves"] #アラート対象通貨
lowalert = {"Bitcoin":400000,"Ethereum":30000,"Litecoin":4200,"NEM":25,"IOTA":80,"Dash":20000,"Lisk":220,"Waves":400,
            "OmiseGo":600,"Civic":50,"Status":6,"NEO":4000} #〇円よりも低いときアラート
hihalert = {"Ethereum":35000,"InsureX":50,"NEM":30,"MonaCoin":60,"Stox":250,"NEO":5500,"CoinDash":20,"TenX":500} #〇円よりも高いときアラート
########################################################################

flaglist = {}
for coin in coinList:
    flaglist.update({coin:0})

coinyen = {}
url = "https://coinmarketcap.com/all/views/all/#JPY"

lineurl = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ token}

while (1):
    #web
    target_html = requests.get(url).text
    html = lxml.html.fromstring(target_html)
    #exchangerate = float(re.findall('data-jpy="([0-9]+.[0-9]+)', target_html)[0])
    exchangerate = 0.009129957970117057

    for coin in coinList:
        xpath = '//*[@id="id-' + coin.lower()  + '"]'
        try:
            priceUSD = float(html.xpath(xpath + "/td[5]/a")[0].text[1:])
        except:
            continue
        priceJPY = priceUSD / exchangerate
        coinyen.update({coin: round(priceJPY,1)})

    print coinyen

    #LINEに送信
    for coin, lowprice in lowalert.items():
        if coinyen[coin] < lowprice and flaglist[coin] == 0:
            message = coin + " is down to " + str(coinyen[coin]) + "円"
            print message + "        "  + str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            payload = {"message": message}
            #files = {"imageFile": open("test.jpg", "rb")}
            r = requests.post(lineurl, headers=headers, params=payload)
            flaglist[coin] = 1
            thread1 = threading.Thread(target=sleeptime, name=coin, args=(coin,))
            thread1.start()

    for coin, highprice in hihalert.items():
        if coinyen[coin] > highprice and flaglist[coin] == 0:
            message = coin + " is up to " + str(coinyen[coin]) + "円"
            print message + "        "  + str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            payload = {"message": message}
            #files = {"imageFile": open("test.jpg", "rb")}
            r = requests.post(lineurl, headers=headers, params=payload)
            flaglist[coin] = 1
            thread1 = threading.Thread(target=sleeptime, name=coin, args=(coin,))
            thread1.start()
    time.sleep(cycle*60)