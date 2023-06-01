<<<<<<< HEAD
from decimal import Decimal
from dotenv import load_dotenv
from pybithumb import Bithumb
from dbConnection import *
from parameter import *
from lib import * 
from sql import *
import requests
import json
import os 

load_dotenv()
secretKey = os.environ.get('SECLET_KEY')
connenctKey = os.environ.get('CONNECT_KEY')

class bitLib():
    def __init__(self):
      self.bithumb = Bithumb(connenctKey, secretKey)

    def checkAccount(self): #보유 예수금 목록
      KRW = self.bithumb.get_balance('BTC')
      KRW = KRW[2]
      return KRW
    
    def getBitCoinList(self, coin): #코인 리스트, 코인 정보 가져오기
      url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
      headers = {"accept": "application/json"}
      response = json.loads(requests.get(url, headers=headers).text)
      return response

    def getMoney(self, coinList):
      money = 0
      list = []
      for i in coinList:
        coinInfo = self.getBitCoinList(str(i[0]).replace('total_',""))
        coinValue = float(coinInfo['data']['closing_price']) * round(float(i[1]), 4)
        list.append(coinValue)
      for index in range(len(list)):
        money += list[index]
      account = self.checkAccount()
      money += account
      return money
    
    def get_ticker_unit(self, price):
      try:
        if Decimal(str(price)) < 10: ticker_unit = 0.01
        elif Decimal(str(price)) < 100: ticker_unit = 0.1
        elif Decimal(str(price)) < 1000: ticker_unit = 1
        elif Decimal(str(price)) < 10000: ticker_unit = 5
        elif Decimal(str(price)) < 100000: ticker_unit = 10
        elif Decimal(str(price)) < 500000: ticker_unit = 50
        elif Decimal(str(price)) < 1000000: ticker_unit = 100
        elif Decimal(str(price)) < 2000000: ticker_unit = 500
        else: ticker_unit = 1000
        return ticker_unit
    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
      except Exception:
        raise
=======
from dotenv import load_dotenv
from pybithumb import Bithumb
from dbConnection import *
from parameter import *
from lib import * 
from sql import *
import requests
import json
import os 

load_dotenv()
secretKey = os.environ.get('SECLET_KEY')
connenctKey = os.environ.get('CONNECT_KEY')

class bitLib():
    def __init__(self):
      self.bithumb = Bithumb(connenctKey, secretKey)

    def checkAccount(self): #보유 예수금 목록
      KRW = self.bithumb.get_balance('BTC')
      KRW = KRW[2]
      return KRW
    
    def getBitCoinList(self, coin): #코인 리스트, 코인 정보 가져오기
      url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
      headers = {"accept": "application/json"}
      response = json.loads(requests.get(url, headers=headers).text)
      return response

    def getMoney(self, coinList):
      money = 0
      list = []
      for i in coinList:
        coinInfo = self.getBitCoinList(str(i[0]).replace('total_',""))
        coinValue = float(coinInfo['data']['closing_price']) * round(float(i[1]), 4)
        list.append(coinValue)
      for index in range(len(list)):
        money += list[index]
      account = self.checkAccount()
      money += account
      return money
>>>>>>> f17ec61ec8279408b0589b3154aebc49b8af8d2c
