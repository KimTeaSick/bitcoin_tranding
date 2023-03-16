from pymongo import MongoClient
import pandas as pd
import numpy as np
import requests
import json
import math

class MongoDB():
    client = MongoClient("mongodb://192.168.10.204:27017/")
    mydb = client["nc_bit_trading"]

    def getAvgData(self, avgRange, coin, term):
        trend = True
        pd.set_option('mode.chained_assignment',  None)
        url = f"https://api.bithumb.com/public/candlestick/"+coin+"_KRW/"+term
        headers = {"accept": "application/json"}
        data = json.loads(requests.get(url, headers=headers).text)['data']
        df = pd.DataFrame(data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
        AR = df['Close'].rolling(window=avgRange).mean().fillna('undefined')
        response = tuple(AR)[-121:-1]
        for index in range(0, 2):
            if response[-index] > float(df['Close'][len(df)-(index+1)]):
                trend = False
        print("trend",trend)
        return {trend, response}
    