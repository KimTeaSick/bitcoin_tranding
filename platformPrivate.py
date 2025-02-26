from utils.searchCondition import optionStandardization
from sqlalchemy.orm import Session
from database import SessionLocal
from returnValue import changer
from dbConnection import MySql
from pybithumb import Bithumb
import pyupbit 
from datetime import datetime
from pandas import DataFrame
from dbConnection import *
from parameter import *
from sqld import *
from utils import *
import recommend
import datetime
import requests
import models
import time
import json

h = "24h"
url = f"https://api.bithumb.com/public/candlestick/BTC_KRW/{h}"
headers = {"accept": "application/json"}

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class UpbitPrivate():
    def __init__(self, connenctKey, secretKey):
        self.upbitPrivate = pyupbit.Upbit(connenctKey, secretKey)
        self.upbit = pyupbit
        self.mysql = MySql()

    def getMyCoinList(self):
        myCoinList = []
        coinList = self.upbitPrivate.get_balances()
        print(coinList)
        for coin in coinList: 
            if coin['currency'] == 'KRW': continue
            myCoinList.append((coin['currency'], coin['balance'], coin['avg_buy_price'], float(coin['balance']) * float(coin['avg_buy_price'])))
        return myCoinList
    
    def myProperty(self):
        coinList = self.upbitPrivate.get_balances()
        money = 0
        account = 0
        for coin in coinList: 
            if coin['currency'] == 'KRW': 
                money += float(coin['balance'])
                account += float(coin['balance'])
            else: 
                nowCoinPrice = pyupbit.get_current_price(ticker=f"KRW-{coin['currency']}")
                money += (nowCoinPrice * float(coin['balance']))
        return money, account

    async def nowRateFn(self, idx):
        myCoinList = self.getMyCoinList()
        revenue = 0
        property_value = 0
        for coin in myCoinList: 
            nowCoinPrice = pyupbit.get_current_price(ticker=f"KRW-{coin[0]}")
            revenue += (nowCoinPrice * float(coin[1])) - coin[3]
            property_value += coin[3]
            print(revenue)
        now_balance = self.myProperty()[0]
        rate = round((revenue / property_value) * 100, 2)
        print("rate", rate, "now_balance", round(now_balance))
        return {"rate": rate, "now_balance": round(now_balance)}








class BitThumbPrivate():
    def __init__(self, connenctKey, secretKey):
        self.bithumb = Bithumb(connenctKey, secretKey)
        self.mysql = MySql()
    
    # def getMyCoinList(self):
    #   coin_list = self.bithumb.get_balance('All')
    #   coin_list = coin_list['data']
    #   coin_total_list = dict.items(coin_list)
    #   my_coin_list = []
    #   for item in coin_total_list:
    #       if 'total_' in str(item[0]) and float(item[1]) >= 0.0001:
    #           if item[0] != 'total_krw' and item[0] != 'total_bm':
    #               my_coin_list.append(item)
    #   print("my_coin_list", my_coin_list)
    #   return my_coin_list

    def getBitCoinList(self, coin):  # 코인 리스트, 코인 정보 가져오기
        url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
        headers = {"accept": "application/json"}
        response = json.loads(requests.get(url, headers=headers).text)
        return response

    def getCandleStick(self, item):  # 차트 데이터
        dataList = []
        url = f"https://api.bithumb.com/public/candlestick/{item.id}_KRW/{item.term}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response = json.loads(response)
        if type(response) == dict:
            response = response['data']
            df = DataFrame(response, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
            for i in range(0, len(df)):
                data = df.iloc[i]
                data.Date = int(data.Date)
                data.Open = float(data.Open)
                data.Close = float(data.Close)
                data.High = float(data.High)
                data.Low = float(data.Low)
                data.Volume = float(data.Volume)
                dataList.append(data)
            _d = tuple(dataList)
            return _d[-121:-1]

    def checkAccount(self):  # 보유 예수금 목록
        try:
            response = self.bithumb.get_balance('BTC')
            KRW = response[2]
            return KRW
        except Exception as e:
            print("checkAccount Error :::: ", e)
            return 444

    def getMyCoinList(self):  # 현재 보유 코인 종류
        coinList = self.bithumb.get_balance('All')
        coinList = coinList['data']
        coinTotalList = dict.items(coinList)
        totalList = []
        myCoinList = []
        for item in coinTotalList:
            if ('total_' in str(item[0])):
                totalList.append(item)
        for item in totalList:
            if (float(item[1]) >= 0.0001):
                if item[0] != 'total_krw':
                    if item[0] != 'total_bm':
                        myCoinList.append(item)
        return myCoinList

    def coinNameList(self):
        coinNames = self.bithumb.get_tickers()
        for index in range(len(coinNames)):
            coinNames[index] += "_KRW"
        return coinNames

    def myProperty(self):
        coinList = self.getMyCoinList()
        list = []
        money = 0
        for i in coinList:
            coinInfo = self.getBitCoinList(str(i[0]).replace('total_', ""))
            if int(coinInfo['status']) == 5500:
                continue
            coinValue = float(
                coinInfo['data']['closing_price']) * round(float(i[1]), 4)
            list.append(coinValue)
        for index in range(len(list)):
            money += list[index]
        account = self.checkAccount()
        money += account
        return money, account

# Dash Page
    async def getRecommendCoin(self, item):
        use_option_list, options, max_minute, max_hour = await optionStandardization.option_standardization(item)
        print("--------------------------------------------------------------------------------------------------")
        # 검색 코인 receive
        coins = await recommend.recommendCoin(options, max_minute, max_hour)
        if coins == 444: return coins
        return {"coins": coins, "optionList": use_option_list}

    async def possessoionCoinInfo(self):
        try:
            possessionCoin = await self.mysql.Select(getMyCoinListSql)
            time.sleep(1)
            if len(possessionCoin) == 0:
                return 203
            else:
                returnList = []
                for coin in possessionCoin:
                    coinInfo = self.getBitCoinList(coin[1])['data']
                    coinValue = float(coinInfo['closing_price'])
                    returnList.append(
                        changer.POSSESSION_COIN_LIST(coin, coinValue))
                print("returnListreturnList", returnList)
                return returnList
        except Exception as e:
            print("possessoionCoinInfo Error :::: ", e)
            return 333

# Auto But and Selling
    async def buy(self, coin, price, unit):  # 매수
        print('buy ::::::: ',coin, price, unit)
        print('----------------------------------------------------------------')
        buyLog = self.bithumb.buy_limit_order(coin, price, unit)  # params 1: 종목, 2: 가격, 3: 갯수
        time.sleep(0.1)
        print(buyLog)
        returnLog = list(buyLog)
        return returnLog

    async def todayAccount(self, idx): 
        try:
            total_revenue = 0
            possession_coin_list = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == idx).all()
            for possession_coin in possession_coin_list:       
                coin_info = self.getBitCoinList(possession_coin.coin)
                if int(coin_info['status']) == 5500:
                    continue
                buy_at_coin_value = float(possession_coin.price) * round(float(possession_coin.unit), 4)
                now_coin_value = float(coin_info['data']['closing_price']) * round(float(possession_coin.unit), 4)
                revenue = now_coin_value - buy_at_coin_value
                total_revenue += revenue
            dt = str(datetime.datetime.now().replace())
            start_dt = dt[0:10] + " 00:00:00.000000"
            end_dt = dt[0:10] + " 23:59:59.999999"
            total_and_deposit = self.myProperty()
            today_buy_price = await self.mysql.Select(todayBuyPrice(start_dt, end_dt, str(idx)))
            today_sell_price = await self.mysql.Select(todaySellPrice(start_dt, end_dt, str(idx)))
            return changer.TODAY_TRADING_RESULT([today_buy_price, today_sell_price, total_and_deposit[0], total_and_deposit[1], total_revenue])
        except Exception as e:
            print(e)

    async def nowRateFn(self, idx):
        try:
            total_revenue = 0
            investment_amount = 0
            property_value = 0
            coin_list = self.getMyCoinList()
            possession_coin_list = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == idx).all()
            for possession_coin in possession_coin_list:   
                coin_info = self.getBitCoinList(possession_coin.coin)
                if int(coin_info['status']) == 5500:
                    continue
                buy_at_coin_value = float(possession_coin.price) * round(float(possession_coin.unit), 4)
                now_coin_value = float(coin_info['data']['closing_price']) * round(float(possession_coin.unit), 4)
                revenue = now_coin_value - buy_at_coin_value
                investment_amount += buy_at_coin_value
                total_revenue += revenue
            for coin in coin_list:
                coin_name = str(coin[0]).replace('total_', '')
                coin_info = self.getBitCoinList(coin_name)
                if int(coin_info['status']) == 5500:
                    continue
                coin_value = float(coin_info['data']['closing_price']) * round(float(coin[1]), 4)
                property_value += coin_value
            now_balance = self.myProperty()[0]
            rate = round((total_revenue / property_value) * 100, 2)
            print("rate", rate, "now_balance", round(now_balance))
            return {"rate": rate, "now_balance": round(now_balance)}
        except Exception as e:
            db.rollback()
            print("nowRateFn ::: ",e)

    async def getBithumbCoinList(self):
        try:
            row_coin_list = await self.mysql.Select(get_bithumb_coin_list_sql)
            coin_list = changer.BITHUMB_COIN_LIST(row_coin_list)
            with open('/data/4season/nc_bit_trading/src/variables/coin_list.json', 'w', encoding="utf-8") as make_file:
                json.dump(coin_list, make_file, ensure_ascii=False, indent="\t")
            return coin_list
        except Exception as e:
            print("Error :::: ", e)
            return
        
        # order_currency
        # price
        # unit

    def sellLimitOrder(self, coin, coinPrice, coinUnit):
        print("coin", coin)
        orderId = self.bithumb.sell_limit_order(coin, coinPrice, coinUnit, "KRW")
        print("orderId",orderId)
        return orderId
    
    def sellMarketOrder(self, coin, coinUnit):
        print("coin", coin)
        orderId = self.bithumb.sell_market_order(coin, coinUnit, "KRW")
        print("orderId",orderId)
        return orderId
