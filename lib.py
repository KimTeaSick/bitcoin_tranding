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