import recommend
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
import asyncio
import requests
import askingPrice
import json
from pybithumb import Bithumb
import time

# 빗썸 api 키
secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"
bithumb = Bithumb(connenctKey, secretKey)


now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

# 검색 함수 실행
async def recommendCoins(options, mMax, hMax):
    coins = await recommend.recommendCoin(options, mMax, hMax)
    return coins

# 사용 db 가져오기 
possessionCoins = db.query(models.possessionCoin).all()
useRecommendOPtion = db.query(models.searchOption).filter(models.searchOption.used == 1).first()
useTradingOption = db.query(models.tradingOption).filter(models.tradingOption.used == 1).first()

# 보유코인 갯수
coinCount = len(possessionCoins)
hadCoin = []
for coin in possessionCoins:
    hadCoin.append(coin.coin)

# 매수 조건
accountOtion = db.query(models.tradingAccountOtion).filter(models.tradingAccountOtion.name == useTradingOption.name).first()
buyOtion = db.query(models.tradingBuyOption).filter(models.tradingBuyOption.name == useTradingOption.name).first()

# 보유 코인 지정 갯수 초과시 종료
if coinCount > accountOtion.price_count:
    print('exit')
    print(accountOtion.price_count, 'maximum')
    print(coinCount, 'have')
    exit()


# 검색 조건
priceOtion = db.query(models.PriceOption).filter(models.PriceOption.name == useRecommendOPtion.name).first()
transactionAmountOption = db.query(models.TransactionAmountOption).filter(models.TransactionAmountOption.name == useRecommendOPtion.name).first()
maspOtion = db.query(models.MASPOption).filter(models.MASPOption.name == useRecommendOPtion.name).first()
trendOption = db.query(models.TrendOption).filter(models.TrendOption.name == useRecommendOPtion.name).first()
disparityOtion = db.query(models.DisparityOption).filter(models.DisparityOption.name == useRecommendOPtion.name).first()
macdOption = db.query(models.MACDOption).filter(models.MACDOption.name == useRecommendOPtion.name).first()

# 검색
mMax:int = 0
hMax:int = 0
options: list = []

# 검색에 필요한 정보 설정
if priceOtion.flag == 1:
    if priceOtion.high_price != 0:
        if 5 > mMax:
            mMax = 5

        options.append({'option': 'Price', 'low_price': priceOtion.low_price, 'high_price': priceOtion.high_price})

if transactionAmountOption.flag == 1:
    if transactionAmountOption.high_transaction_amount != 0:
        if transactionAmountOption.chart_term[-1] == 'm' and int(transactionAmountOption.chart_term[:-1]) > mMax:
            mMax = int(transactionAmountOption.chart_term[:-1])

        if transactionAmountOption.chart_term[-1] == 'h' and int(transactionAmountOption.chart_term[:-1]) > hMax:
            hMax = int(transactionAmountOption.chart_term[:-1])

    options.append({'option':'TransactionAmount', 'chart_term':transactionAmountOption.chart_term, 'low_transaction_amount':transactionAmountOption.low_transaction_amount, 'high_transaction_amount':transactionAmountOption.high_transaction_amount})

if maspOtion.flag == 1:
    if maspOtion.first_disparity != 0 and maspOtion.second_disparity != 0:
        print('first_disparity: ', maspOtion.first_disparity, 'second_disparity: ', maspOtion.second_disparity)

        if maspOtion.chart_term[-1] == 'm' and (maspOtion.first_disparity * int(maspOtion.chart_term[:-1])) > mMax:
            mMax = maspOtion.first_disparity * int(maspOtion.chart_term[:-1])
        if maspOtion.chart_term[-1] == 'm' and (maspOtion.second_disparity * int(maspOtion.chart_term[:-1])) > mMax:
            mMax = maspOtion.second_disparity * int(maspOtion.chart_term[:-1])

        if maspOtion.chart_term[-1] == 'h' and (maspOtion.first_disparity * int(maspOtion.chart_term[:-1])) > hMax:
            hMax = (maspOtion.first_disparity) * int(maspOtion.chart_term[:-1])
        if maspOtion.chart_term[-1] == 'h' and (maspOtion.second_disparity * int(maspOtion.chart_term[:-1])) > hMax:
            hMax = (maspOtion.second_disparity) * int(maspOtion.chart_term[:-1])

        options.append({'option': 'MASP', 'chart_term': maspOtion.chart_term, 'first_disparity': maspOtion.first_disparity, 'second_disparity': maspOtion.second_disparity, 'comparison': maspOtion.comparison})

if disparityOtion.flag == 1:
    if disparityOtion.chart_term != 0:
        if disparityOtion.chart_term[-1] == 'm' and (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1])) > mMax:
            mMax = (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1]))

        if disparityOtion.chart_term[-1] == 'h' and (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1])) > hMax:
            hMax = (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1]))

        options.append({'option':'Disparity', 'chart_term': disparityOtion.chart_term, 'disparity_term':disparityOtion.disparity_term, 'low_disparity': disparityOtion.low_disparity, 'high_disparity': disparityOtion.high_disparity})

if trendOption.flag == 1:
    if trendOption.trend_term != 0 and trendOption.MASP != 0:
        if trendOption.chart_term[-1] == 'm' and ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1])) > mMax:
            mMax = ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1]))

        if trendOption.chart_term[-1] == 'h' and int((int(trendOption.trend_term) + 2 + int(trendOption.MASP)) * int(trendOption.chart_term[:-1])) > hMax:
            hMax = ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1]))

        options.append({'option':'Trend', 'chart_term': trendOption.chart_term, 'trend_term': trendOption.trend_term, 'trend_type': trendOption.trend_type, 'trend_reverse': trendOption.trend_reverse, "MASP": trendOption.MASP})

if macdOption.flag == 1:
    if macdOption.short_disparity != 0 and macdOption.long_disparity != 0:
        if macdOption.chart_term[-1] == 'm' and ((macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])) > mMax:
            mMax = (macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])

        if macdOption.chart_term[-1] == 'h' and ((macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])) > hMax:
            hMax = (macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])

        options.append({'option':'MACD', 'chart_term':macdOption.chart_term, 'short_disparity':macdOption.short_disparity, 'long_disparity':macdOption.long_disparity,'signal':macdOption.signal, 'up_down':macdOption.up_down})

print(options)
print(f'mMax: {mMax}, hMax: {hMax}')

db.query(models.recommendList).delete()

# 검색 함수 실행
coins = asyncio.run(recommendCoins(options, mMax, hMax))
print('----------------------------------------------------------------------------------검색 완료')

# 코인 disparity 순으로 정렬 / 검색된 코인 insert
sortedByDisparity = []
for coin in coins['recommends']:
    print("asdasdasdas", useRecommendOPtion.name)
    coinName = list(coin.keys())[0]
    sortedByDisparity.append({'name': coinName,'disparity': coin[coinName]['disparity'], 'price': coin[coinName]['closing_price']})

    RCCoin = models.recommendList()
    RCCoin.coin_name = coinName
    RCCoin.catch_price = coin[coinName]['closing_price']
    RCCoin.option_name = useRecommendOPtion.name
    db.add(RCCoin)

sortedCoins = sorted(sortedByDisparity, key=lambda x:x['disparity'])
print(sortedCoins)

# 거래 가능 금액 가져오기
money = bithumb.get_balance('BTC')[2]
print(money,'333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')
moneyPerCoin:float = 0

# 코인당 거래할 금액 계산
if buyOtion.checkbox == 1:
    moneyPerCoin = buyOtion.price_to_buy_method * 10000
elif buyOtion.checkbox == 2:
    moneyPerCoin = (money * buyOtion.percent_to_buy_method) / 100

print(f'moneyPerCoin: {moneyPerCoin}, money: {money}, percent: {buyOtion.percent_to_buy_method}')

orders = ''
orderList = []
print(money)
for coin in sortedCoins:
    try:
        # 구매 안하는 사유
        if coinCount >= int(accountOtion.price_count):
            print('coin count')
            coin['fail_reason'] = 'coin count'
            continue

        if moneyPerCoin > money:
            print('money')
            coin['fail_reason'] = 'money'
            continue

        if coin['name'] in hadCoin:
            print('보유 코인')
            coin['fail_reason'] = 'possession coin'
            continue

        print(coinCount, accountOtion.price_count, coin['name'])

        orders = ''

        # 지정 호가 계산
        ask = askingPrice.askingPrice(int(float(coin['price'])))
        splitBuy = moneyPerCoin * 1
        askPrice = float(coin['price']) + (buyOtion.callmoney_to_buy_method * ask)
        askPrice = (round(askPrice,4))
        splitUnit = splitBuy / (float(askPrice))

        # 주문
        order = bithumb.buy_limit_order(coin['name'], float(askPrice), round(splitUnit, 4), 'KRW')
        print(order)

        order_id = order[2]

        # 주문 가능한 금액 계산, 보유코인 1개 추가
        money -= moneyPerCoin
        coinCount += 1
        orderList.append({'coin': coin['name'], 'orders': order_id})
        coin['orders'] = order_id
    except Exception as e:
        print(e)

print(orderList)
for ordercheck in orderList:
    print(ordercheck['coin'])
    # 보유코인, 주문 내역 테이블에 추가
    orderID = ordercheck['orders'].split(',')[:-1]
    unit = 0.0
    total = 0.0
    fee = 0.0

    i = 0
    # 주문 테이블 추가
    order_coin = models.orderCoin()
    order_coin.coin = ordercheck['coin']
    order_coin.status = 1
    order_coin.transaction_time = datetime.datetime.now()
    order_coin.order_id = ordercheck['orders']
    order_coin.cancel_time = (datetime.datetime.now() + datetime.timedelta(seconds = accountOtion.buy_cancle_time))
    db.add(order_coin)

    # 보유코인 추가
    possession_coin = models.possessionCoin()
    possession_coin.coin = ordercheck['coin']
    possession_coin.unit = 0.0
    possession_coin.price = 0.0
    possession_coin.total = 0.0
    possession_coin.fee = 0.0
    possession_coin.status = 1
    possession_coin.transaction_time = datetime.datetime.now()
    possession_coin.order_id = ordercheck['orders']
    possession_coin.cancel_time = (datetime.datetime.now() + datetime.timedelta(seconds = accountOtion.buy_cancle_time))
    possession_coin.macd_chart = macdOption.chart_term
    possession_coin.disparity_chart = disparityOtion.chart_term
    possession_coin.optionName = useRecommendOPtion.name
    db.add(possession_coin)

try:
    db.commit()
except Exception as e:
    print(e)
    db.rollback()

with open("./buyLog", "a") as file:
    file.write(f'{datetime.datetime.now()}------------------------------------------------------------------')
    for buyCoin in sortedCoins:
        file.write(str(buyCoin) + '\n')
    file.close()


now2 = datetime.datetime.now()
print(now2-now1)
