import json
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
import requests
import askingPrice
import json
from pybithumb import Bithumb
import time
import pandas as pd
import numpy as np

now1 = datetime.datetime.now()

# api url
bithumbApi = 'https://api.bithumb.com/public/ticker/'

secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"
bithumb = Bithumb(connenctKey, secretKey)

headers = {"accept": "application/json"}

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

possession_coins = db.query(models.possessionCoin).all()
useTradingOption = db.query(models.tradingOption).filter(
    models.tradingOption.used == 1).first()
accountOtion = db.query(models.tradingAccountOtion).filter(
    models.tradingAccountOtion.name == useTradingOption.name).first()
sellOption = db.query(models.tradingSellOption).filter(
    models.tradingSellOption.name == useTradingOption.name).first()

autoStatus = db.query(models.autoTradingStatus).filter(
    models.autoTradingStatus.status == 1).first()

if autoStatus == None:
    print('exit')
    print('자동매매 정지')
    exit()

chartMax = 0
for possession in possession_coins:
    if chartMax < int(possession.macd_chart[:-1]):
        chartMax = int(possession.macd_chart[:-1])

    if chartMax < int(possession.disparity_chart[:-1]):
        chartMax = int(possession.disparity_chart[:-1])

max = 0
if (sellOption.disparity_for_upper_case * chartMax) > max:
    max = sellOption.disparity_for_upper_case * chartMax
if (sellOption.disparity_for_down_case * chartMax) > max:
    max = sellOption.disparity_for_down_case * chartMax
if ((sellOption.long_MACD_value + sellOption.MACD_signal_value) * chartMax) > max:
    max = (sellOption.long_MACD_value +
           sellOption.MACD_signal_value + 1) * chartMax

print(sellOption.disparity_for_upper_case, sellOption.disparity_for_down_case)
max += 10
print(max)

possession: float = 0.0
nowWallet = 0.0
isSell = []
resale = []

# 총 구매 금액 계산
for coins in possession_coins:
    possession += float(coins.total)
    response = json.loads(requests.get(
        bithumbApi + coins.coin+'_KRW', headers=headers).text)
    nowPrice = float(response['data']['closing_price']) * float(coins.unit)
    ask = askingPrice.askingPrice(float(response['data']['closing_price']))

    if coins.status == 4:
        if float(coins.total) != 0.0 or float(nowPrice) != 0.0:
            resale.append({'coin': coins.coin, 'nowprice': response['data']['closing_price'], 'unit': coins.unit, 'buyPrice': coins.price, 'percent': (
                nowPrice / float(coins.total)) * 100 - 100, 'ask': ask, 'macd_chart': coins.macd_chart, 'disparity_chart': coins.disparity_chart})

    else:
        if float(coins.total) != 0.0 or float(nowPrice) != 0.0:
            isSell.append({'coin': coins.coin, 'nowprice': response['data']['closing_price'], 'unit': coins.unit, 'buyPrice': coins.price, 'percent': (
                nowPrice / float(coins.total)) * 100 - 100, 'ask': ask, 'macd_chart': coins.macd_chart, 'disparity_chart': coins.disparity_chart})

    nowWallet += nowPrice


print(possession, '구매가')
print(nowWallet, '현재가')
print(isSell)

sellReason = []

try:
    percent = (nowWallet / possession) * 100 - 100
except Exception as e:
    print(e)
    percent = 0

print(percent, 'gggggggggggggggggggggggggggggggggggggggggggggggggggg')
print(accountOtion.loss_cut_under_percent)
'''
# 매도 취소 재매도
for sell in resale:
    sellReason.append({'coin': sell['coin'], 'reason': 'resale', 'unit': sell['unit'], 'close': sell['nowprice'],
                      'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})

# 로스컷 or autosell
if float(percent) >= float(accountOtion.loss_cut_over_percent):
    print('로스컷 오버')
    for sell in isSell:
        if sell['percent'] >= accountOtion.loss_cut_over_coin_specific_percent and accountOtion.gain == 2:
            sellReason.append({'coin': sell['coin'], 'reason': 'loss cut over', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_over_call_price_specific_coin})

        if accountOtion.gain == 1:
            sellReason.append({'coin': sell['coin'], 'reason': 'loss cut over', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_over_call_price_sell_all})

        print('로스컷 오버 판매 완료')


elif float(percent) <= -float(accountOtion.loss_cut_under_percent):
    print('로스컷 언더')
    for sell in isSell:
        if sell['percent'] <= accountOtion.loss_cut_under_coin_specific_percent and accountOtion.loss == 2:
            sellReason.append({'coin': sell['coin'], 'reason': 'loss cut under', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_under_call_price_specific_coin})

        if accountOtion.loss == 1:
            sellReason.append({'coin': sell['coin'], 'reason': 'loss cut under', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_under_call_price_sell_all})

        print('로스컷 언더 판매')
'''
# 로스컷 아닐 때 판매 조건
# else:
if True:  # 기준가격 미만 조건만 남김 0712
    print('passing loss cut process')
    print('매도 시작')
    sellList = []

    for sell in isSell:
        '''
        print(sell['coin'])
        # 매도조건 1. 가격기준 / 상승
        if sell['percent'] >= sellOption.upper_percent_to_price_condition:
            sellReason.append({'coin': sell['coin'], 'reason': 'price over', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})
            continue
        '''

        # 매도조건 1. 가격기준 / 하락
        # elif sell['percent'] <= (- sellOption.down_percent_to_price_condition):
        if sell['percent'] <= (- sellOption.down_percent_to_price_condition):
            print((- sellOption.down_percent_to_price_condition))
            sellReason.append({'coin': sell['coin'], 'reason': 'price under', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})
            continue
        '''
        nowstamp = int(int(now1.timestamp()) / 60) * 60  # + (60*540)
        print(nowstamp, '============================================================')
        hNowStamp = nowstamp - (max * 3600)
        dfhList = []
        dfhSource = db.query(models.coin1HPrice).filter(models.coin1HPrice.STime >= hNowStamp).filter(
            models.coin1HPrice.coin_name == sell['coin'] + '_KRW').all()
        for dfs in dfhSource:
            dfhList.append({'idx': dfs.idx, 'coin_name': dfs.coin_name, 'S_time': int(dfs.STime), 'time': dfs.time, 'Close': float(
                dfs.Close), 'Volume': float(dfs.Volume), 'Transaction_amount': float(dfs.Close) * float(dfs.Volume)})

        df = pd.DataFrame(dfhList)

        df['time'] = pd.to_datetime(df['time'])

        df = df.set_index('time').resample('1H').asfreq()
        df = df.fillna(method='ffill')

        dfx = df[(len(df) % int(sell['disparity_chart'][:-1])):]
        dfx.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        new_df = dfx.groupby(np.arange(
            len(dfx)) // int(sell['disparity_chart'][:-1])).mean(numeric_only=True)

        df2 = new_df[len(new_df)-sellOption.disparity_for_upper_case:]
        avgUpper = df2['Close'].mean()

        df3 = new_df[len(new_df)-sellOption.disparity_for_down_case:]
        avgDown = df3['Close'].mean()

        upDisp = (float(avgUpper) / float(sell['nowprice'])) * 100 - 100
        dnDisp = (float(avgDown) / float(sell['nowprice'])) * 100 - 100

        print(upDisp, dnDisp)
        if upDisp > sellOption.upper_percent_to_disparity_condition:
            sellReason.append({'coin': sell['coin'], 'reason': 'disparity over', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})
            continue

        if upDisp > sellOption.down_percent_to_disparity_condition:
            sellReason.append({'coin': sell['coin'], 'reason': 'disparity under', 'unit': sell['unit'], 'close': sell['nowprice'],
                              'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})
            continue

        if sell['nowprice'] > sell['buyPrice']:
            print(
                'MACD-----------------------------------------------------------------------')
            # 매도 조건 Macd
            dfy = df[(len(df) % int(sell['macd_chart'][:-1])):]
            dfy.reset_index(drop=True, inplace=True)

            # 리스트를 times개씩 묶기
            new_df2 = dfy.groupby(
                np.arange(len(dfy)) // int(sell['macd_chart'][:-1])).mean(numeric_only=True)
            print(new_df2)

            # short EMA 계산
            emashort = new_df2['Close'].ewm(
                span=int(sellOption.shot_MACD_value)).mean()
            # long EMA 계산
            emalong = new_df2['Close'].ewm(
                span=int(sellOption.long_MACD_value)).mean()
            # MACD 계산
            macd = emashort - emalong

            macdSignal = macd.ewm(
                span=int(sellOption.MACD_signal_value)).mean()
            macdOscillator = macd - macdSignal

            if macdOscillator.iloc[-2] > 0 and macdOscillator.iloc[-1] < 0:
                sellReason.append({'coin': sell['coin'], 'reason': 'macd signal', 'unit': sell['unit'], 'close': sell['nowprice'],
                                  'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': sellOption.call_money_to_sell_method})
                continue
        '''
    print(sell)
    print(sellList, 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')


with open("./sellLog", "a") as file:
    file.write(
        f'{datetime.datetime.now()}------------------------------------------------------------------')
    for reason in sellReason:
        file.write(str(reason) + '\n')
    file.close()

# 매도 주문
for sellOrder in sellReason:
    try:
        if sellOrder['reason'] == 'resale':
            print(sellOrder)
            coin = sellOrder['coin']
            # askP = float(sellOrder['close']) + (int(sellOrder['askprice']) * sellOrder['ask'])

            if sellOption.call_money_to_sell_method > 0:
                ask = f'+{sellOption.call_money_to_sell_method}'
            else:
                ask = str(sellOption.call_money_to_sell_method)
            askP = askingPrice.ASK_PRICE(
                f"{sellOrder['coin']}_KRW", ask, 'sell')

            orderids = bithumb.sell_limit_order(
                sellOrder['coin'], float(askP), float(sellOrder['unit']), "KRW")
            print(
                f'{coin} 매도주문 56666666666666666666666666666666666666666666666666666666666666666666')
            print(orderids)

            order_coin = models.orderCoin()
            order_coin.coin = sellOrder['coin']
            order_coin.status = 5
            order_coin.transaction_time = datetime.datetime.now()
            order_coin.order_id = orderids[2]
            order_coin.cancel_time = (datetime.datetime.now(
            ) + datetime.timedelta(seconds=accountOtion.buy_cancle_time))
            order_coin.sell_reason = sellOrder['reason']
            db.add(order_coin)

            db.commit()

        else:
            print(sellOrder)
            coin = sellOrder['coin']
            # askP = float(sellOrder['close']) + (int(sellOrder['askprice']) * sellOrder['ask'])

            if sellOption.call_money_to_sell_method > 0:
                ask = f'+{sellOption.call_money_to_sell_method}'
            else:
                ask = str(sellOption.call_money_to_sell_method)
            askP = askingPrice.ASK_PRICE(
                f"{sellOrder['coin']}_KRW", ask, 'sell')

            orderids = bithumb.sell_limit_order(
                sellOrder['coin'], float(askP), float(sellOrder['unit']), "KRW")
            print(
                f'{coin} 매도주문 56666666666666666666666666666666666666666666666666666666666666666666')
            print(orderids)

            order_coin = models.orderCoin()
            order_coin.coin = sellOrder['coin']
            order_coin.status = 3
            order_coin.transaction_time = datetime.datetime.now()
            order_coin.order_id = orderids[2]
            order_coin.cancel_time = (datetime.datetime.now(
            ) + datetime.timedelta(seconds=accountOtion.buy_cancle_time))
            order_coin.sell_reason = sellOrder['reason']
            db.add(order_coin)

            db.commit()

    except Exception as e:
        print(e, 'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        pass
