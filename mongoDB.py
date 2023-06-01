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
        AR = tuple(df['Close'].rolling(window=avgRange).mean().fillna('undefined'))
        response = AR[-121:-1]
        BASE = df['Close'].values.tolist()
        for index in range(0, 2):
            result = float(BASE[len(BASE) - (index + 1)]) - float(response[len(response) - (index + 1)])
            print(coin, result)
            if result < 0:
                trend = False
        print("trend",trend)
        return {trend, response}
    