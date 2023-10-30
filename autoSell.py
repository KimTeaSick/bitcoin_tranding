from database import engine, SessionLocal
from sqlalchemy.orm import Session
import json
import models
import datetime
import requests
import askingPrice
import json
from pybithumb import Bithumb
from sell.lossOver import LossOverSell
from sell.lossUnder import LossUnderSell
from sell.priceDrop import PriceDropSell
from sell.reSale import ReSaleSell
from sell.oneDollarUnderPriceClean import one_doller_under_price_clean
import time
import pandas as pd
import numpy as np
now1 = datetime.datetime.now()
# api url
bithumbApi = 'https://api.bithumb.com/public/ticker/'
headers = {"accept": "application/json"}
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

active_users = db.query(models.USER_T).filter(models.USER_T.active == 1).all()
print("active_users", active_users)
for active_user in active_users:
    bithumb = Bithumb(active_user.public_key, active_user.secret_key)
    possession_coins = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == active_user.idx).all()
    useTradingOption = db.query(models.tradingOption).filter(
        models.tradingOption.idx == active_user.trading_option).first()
    accountOtion = db.query(models.tradingAccountOption).filter(
        models.tradingAccountOption.idx == useTradingOption.idx).first()
    sellOption = db.query(models.tradingSellOption).filter(
        models.tradingSellOption.idx == useTradingOption.idx).first()

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
    # print(sellOption.disparity_for_upper_case, sellOption.disparity_for_down_case)
    max += 10
    # print(max)

    ### 
    possession: float = 0.0 # 보유 종목 총합 매수 단가
    nowWallet = 0.0 # 보유 종목 총합 현재가
    isSell = [] # 매도 리스트
    resale = [] # 재 매도 리스트
    under_one_dollar = []
    sell_list = []
    ###

    # 총 구매 금액 계산 0, 보유중, 1: 매수 중, 2: 분할 매수, 3: 첫 번째 매도 중, 4: 매도 취소, 5: 매도 중 , 6: 매도 완료
    for coin in possession_coins:
        print(coin.coin)
        possession += float(coin.total)
        response = json.loads(requests.get(bithumbApi + coin.coin + '_KRW', headers=headers).text)
        nowPrice = float(response['data']['closing_price']) * float(coin.unit)
        ask = askingPrice.askingPrice(float(response['data']['closing_price']))
        if float(coin.total) != 0.0 or float(nowPrice) != 0.0:
            if float(coin.total) <= 1000:
                under_one_dollar.append({'coin': coin.coin, 'nowprice': response['data']['closing_price'], 'unit': coin.unit, 'buyPrice': coin.price, 'percent': (
                nowPrice / float(coin.total)) * 100 - 100, 'ask': ask, 'macd_chart': coin.macd_chart, 'disparity_chart': coin.disparity_chart, "total": coin.total })
            elif coin.status == 4 and float(coin.total) >= 1000:
                resale.append({'coin': coin.coin, 'nowprice': response['data']['closing_price'], 'unit': coin.unit, 'buyPrice': coin.price, 'percent': (
                nowPrice / float(coin.total)) * 100 - 100, 'ask': ask, 'macd_chart': coin.macd_chart, 'disparity_chart': coin.disparity_chart})
            else:
                isSell.append({'coin': coin.coin, 'nowprice': response['data']['closing_price'], 'unit': coin.unit, 'buyPrice': coin.price, 'percent': (
                nowPrice / float(coin.total)) * 100 - 100, 'ask': ask, 'macd_chart': coin.macd_chart, 'disparity_chart': coin.disparity_chart})
        nowWallet += nowPrice

    print('구매가', possession)
    print('현재가', nowWallet)
    print('isSell', isSell)
    print("---------------------------------------------------------------------------------------------------------")

    try:
        percent = (nowWallet / possession) * 100 - 100
    except Exception as e:
        print(e)
        percent = 0

    print("percent", percent)
    print("loss cut under percent", accountOtion.loss_cut_under_percent)

    print("---------------------------------------------------------------------------------------------------------")
    print("resale start ::: ::: ")
    # 매도 취소 재매도
    for sell in resale:
        re_sale_coin = ReSaleSell(sell, sellOption)
        sell_list.append(re_sale_coin)
    print("resale end ::: ::: ")

    # 1000원 미만 코인 처리
    print("---------------------------------------------------------------------------------------------------------")
    print("under one dollar clean start ::: ::: ")
    print("under one dollar list ::: ::: ", under_one_dollar)

    if float(percent) <= -float(accountOtion.loss_cut_under_percent):
        for sell in isSell:
            loss_under_coin = LossUnderSell(sell, accountOtion)
            print("loss under coin", loss_under_coin)
            if loss_under_coin == None: pass
            # if sell['percent'] <= accountOtion.loss_cut_under_coin_specific_percent and accountOtion.loss == 2:
            #     sell_list.append({'coin': sell['coin'], 'reason': 'loss cut under', 'unit': sell['unit'], 'close': sell['nowprice'],
            #                     'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_under_call_price_specific_coin})
            # if accountOtion.loss == 1:
            #     sell_list.append({'coin': sell['coin'], 'reason': 'loss cut under', 'unit': sell['unit'], 'close': sell['nowprice'],
            #                     'buyPrice': sell['buyPrice'], 'ask': sell['ask'], 'askprice': accountOtion.loss_cut_under_call_price_sell_all})
                
        print('loss under sell list ::: ::: ', sell_list)
        print('로스컷 언더 판매')

    print("---------------------------------------------------------------------------------------------------------")

    # 로스컷 아닐 때 판매 조건
    # else:
    if True:  # 기준가격 미만 조건만 남김 0712
        print('passing loss cut process')
        print('매도 시작')

        for sell in isSell:
            price_drop_coin = PriceDropSell(sell, sellOption)
            sell_list.append(price_drop_coin)

    with open("./sellLog", "a") as file:
        file.write(
            f'{datetime.datetime.now()}------------------------------------------------------------------')
        for reason in sell_list:
            file.write(str(reason) + '\n')
        file.close()

    # 매도 주문
    print("sell_list", sell_list)
    for sell_order in sell_list:
        print("매도 주문", sell_order)
        try:
            if sell_order['reason'] == 'resale':
                coin = sell_order['coin']
                ask = f'+{sellOption.call_money_to_sell_method}' if int(sellOption.call_money_to_sell_method) >= 0 else str(sellOption.call_money_to_sell_method)
                sell_price = askingPrice.ASK_PRICE(f"{sell_order['coin']}", ask, 'sell')
                # orderids = bithumb.sell_market_order(sell_order['coin'], float(sell_order['unit']), "KRW")
                # order_coin = models.orderCoin()
                # order_coin.coin = sell_order['coin']
                # order_coin.status = 5
                # order_coin.transaction_time = datetime.datetime.now()
                # order_coin.order_id = orderids[2]
                # order_coin.cancel_time = (datetime.datetime.now() + datetime.timedelta(seconds=accountOtion.buy_cancle_time))
                # order_coin.sell_reason = sell_order['reason']
                # order_coin.user_idx = active_user.idx
                # db.add(order_coin)
                # db.commit()
            else:
                coin = sell_order['coin']
                if int(sellOption.call_money_to_sell_method) >= 0:
                    ask = f'+{sellOption.call_money_to_sell_method}'
                else:
                    ask = str(sellOption.call_money_to_sell_method)
                askP = askingPrice.ASK_PRICE(f"{sell_order['coin']}", ask, 'sell')
                # orderids = bithumb.sell_limit_order(sell_order['coin'], round(float(askP), 1), float(sell_order['unit']), "KRW")
                # order_coin = models.orderCoin()
                # order_coin.coin = sell_order['coin']
                # order_coin.status = 3
                # order_coin.transaction_time = datetime.datetime.now()
                # order_coin.order_id = orderids[2]
                # order_coin.cancel_time = (datetime.datetime.now() + datetime.timedelta(seconds=accountOtion.buy_cancle_time))
                # order_coin.sell_reason = sell_order['reason']
                # order_coin.user_idx = active_user.idx
                # db.add(order_coin)
                # db.commit()
        except Exception as e:
            print("sell Error ::: ::: ", e)
            pass
