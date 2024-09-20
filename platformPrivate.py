from utils.searchCondition import optionStandardization
from sqlalchemy.orm import Session
from database import SessionLocal
from returnValue import changer
from dbConnection import MySql
from pybithumb import Bithumb
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

class BitThumbPrivate():
    def __init__(self, connenctKey, secretKey):
        self.bithumb = Bithumb(connenctKey, secretKey)
        self.coinList = list(self.getBitCoinList('ALL')['data'].keys())[0:-1]
        self.recommandCoinList = []
        self.mysql = MySql()
    
    def get_my_coin_list(self):
      coin_list = self.bithumb.get_balance('All')
      coin_list = coin_list['data']
      coin_total_list = dict.items(coin_list)
      my_coin_list = []
      for item in coin_total_list:
          if 'total_' in str(item[0]) and float(item[1]) >= 0.0001:
              if item[0] != 'total_krw' and item[0] != 'total_bm':
                  my_coin_list.append(item)
      return my_coin_list

    def check_account(self):
        krw_balance = self.bithumb.get_balance('BTC')[2]
        return krw_balance
    
    async def getMyPossessionCoinList(self):
        myCoinList = await self.mysql.Select(getMyCoinListSql)
        return myCoinList

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

    def calndel_for_search(self, item):
        coin = item["id"]
        term = item["term"]
        url = f"https://api.bithumb.com/public/candlestick/{coin}_KRW/{term}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).text
        response = json.loads(response)
        return response

    def getCoinOrderBook(self, coin):  # 코인 거래 내역
        orderBook = self.bithumb.get_orderbook(coin)
        return orderBook

    def checkAccount(self):  # 보유 예수금 목록
        try:
            response = self.bithumb.get_balance('BTC')
            KRW = response[2]
            return KRW
        except Exception as e:
            print("checkAccount Error :::: ", e)
            return 444

    def setBuyCondition(self):  # 매수 조건
        url = f"https://api.bithumb.com/public/ticker/ALL_KRW"
        headers = {"accept": "application/json"}
        response = json.loads(requests.get(url, headers=headers).text)
        allData = list(dict.items(response['data']))[0: -1]
        matchList = []
        for item in allData:
            if float(item[1]["acc_trade_value_24H"]) >= 1000000000.8963:
                if float(item[1]["fluctate_rate_24H"]) >= 3.00:
                    matchList.append(item)
        for item in matchList:
            print(item[0])
        return matchList

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
    
    def getBuyPrice(self, coin):
        buyPrice = self.bithumb.get_orderbook(coin)['bids'][1]['price']
        return buyPrice

    def buyQuantity(self, buyPrice):
        buy_quantity = self.checkAccount() * 0.9970 / buyPrice  # 수수료 0.25% 계산
        buy_quantity = float("{:.4f}".format(buy_quantity))  # 소수점 4자리 수 버림
        return buy_quantity

    def bulkSale(self):
        coinList = self.getMyCoinList()
        for coin in coinList:
            coinName = (str(coin[0]).replace('total_', ""))
            if (coinName != 'krw'):
                coinName = coinName.upper()
                self.sell(coinName, float(coin[1]))

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
        print("item ::: ",item)
        use_option_list, options, max_minute, max_hour = await optionStandardization.option_standardization(item)
        print("--------------------------------------------------------------------------------------------------")
        print("use_option_list, options, max_minute, max_hour",use_option_list, options, max_minute, max_hour)
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

# Setting Page
    async def getSearchOptionList(self):
        value = await self.mysql.Select(selectSearchOptionSql)
        optionList = []
        for data in value:
            optionList.append({
                "idx": data[0],
                "name": data[1],
                "first_disparity": data[2],
                "second_disparity": data[3],
                "trends": data[4],
                "trends_idx": data[5],
                "avg_volume": data[6],
                "transaction_amount": data[7],
                "price": data[8]})
        print(optionList)
        return optionList

    def insertSearchOption(self, item):
        self.mysql.Insert(insertSearchOptionSql, [
            item.name,
            item.first_disparity,
            item.second_disparity,
            item.trends_idx,
            item.trends,
            item.avg_volume,
            item.transaction_amount,
            item.price
        ])

    async def updateSearchOption(self, item):
        await self.mysql.Update(updateSearchOptionSql, [
            item.name,
            item.first_disparity,
            item.second_disparity,
            item.trends_idx,
            item.trends,
            item.avg_volume,
            item.transaction_amount,
            item.price,
            item.idx
        ])

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
            coin_list = self.get_my_coin_list()
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
            return {"rate": rate, "now_balance": round(now_balance)}
        except Exception as e:
            db.rollback()
            print("nowRateFn ::: ", idx, e)

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
