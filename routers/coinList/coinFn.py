from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
import pandas as pd
from sqld import *
import requests
import json
 

class CoinFn():

  async def getDisparityOption(self, bit):
    try:
      options = await bit.mysql.Select(getMASPoptionSql)
      options ={options[0][1]: {"idx": options[0][0], "name": options[0][1], "range": options[0][2], "color": options[0][3]},
                options[1][1]: {"idx": options[1][0], "name": options[1][1], "range": options[1][2], "color": options[1][3]},
                options[2][1]: {"idx": options[2][0], "name": options[2][1], "range": options[2][2], "color": options[2][3]}}
      return options
    except Exception as e:
      print("Error :::::: ", e)
      return 444
    
  async def updateDisparityOption(self, item, bit):
    try:
      for data in item:
          await bit.mysql.Update(updateMASPoptionSql, [str(data[1]['range']), data[1]['color'], data[1]['name']])
      return 200
    except:
      return 303
    
  def getAvgData(self, avgRange, coin, term, bit):
    try:
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
    except Exception as e:
      print("Error :::::: ", e)
      return 333
    