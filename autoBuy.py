import recommend
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
import asyncio
import askingPrice
from pybithumb import Bithumb
from buy.optionStandardization import OptionStandardization
import requests
import time
import json

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

active_users = db.query(models.USER_T).filter(models.USER_T.active == 1).all()

for active_user in active_users:
    bithumb = Bithumb(active_user.public_key, active_user.secret_key)
# 사용 db 가져오기
    possession_coins = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == active_user.idx).all()
    useRecommendOPtion = db.query(models.searchOption).filter(
        models.searchOption.idx == active_user.search_option).first()
    useTradingOption = db.query(models.tradingOption).filter(
        models.tradingOption.idx == active_user.trading_option).first()
    autoStatus = db.query(models.autoTradingStatus).filter(
        models.autoTradingStatus.status == 1).first()
    userIdx = 2

    # 보유코인 갯수
    coinCount = len(possession_coins)
    hadCoin = []
    for coin in possession_coins:
        hadCoin.append(coin.coin)

    # 매수 조건
    accountOption = db.query(models.tradingAccountOption).filter(
        models.tradingAccountOption.idx == useTradingOption.idx).first()
    buyOption = db.query(models.tradingBuyOption).filter(
        models.tradingBuyOption.idx == useTradingOption.idx).first()

    # 보유 코인 지정 갯수 초과시 종료
    if coinCount > accountOption.price_count:
        print('exit')
        print(accountOption.price_count, 'maximum')
        print(coinCount, 'have')
        break

    # 검색 조건
    priceOption = db.query(models.PriceOption).filter(
        models.PriceOption.idx == useRecommendOPtion.idx).first()

    transactionAmountOption = db.query(models.TransactionAmountOption).filter(
        models.TransactionAmountOption.idx == useRecommendOPtion.idx).first()

    maspOption = db.query(models.MASPOption).filter(
        models.MASPOption.idx == useRecommendOPtion.idx).first()

    trendOption = db.query(models.TrendOption).filter(
        models.TrendOption.idx == useRecommendOPtion.idx).first()

    disparityOption = db.query(models.DisparityOption).filter(
        models.DisparityOption.idx == useRecommendOPtion.idx).first()

    macdOption = db.query(models.MACDOption).filter(
        models.MACDOption.idx == useRecommendOPtion.idx).first()

    # 검색
    # 검색에 필요한 정보 설정
    option_result = OptionStandardization( priceOption, transactionAmountOption, maspOption, trendOption, disparityOption, macdOption)
    options: list = option_result[0]
    mMax: int = option_result[1]
    hMax:int  = option_result[2]


    print(options)
    print(f'mMax: {mMax}, hMax: {hMax}')

    prevCoin = db.query(models.recommendList).filter(models.recommendList.user_idx == active_user.idx).all()
    db.delete(prevCoin)

    # 검색 함수 실행
    coins = asyncio.run(recommendCoins(options, mMax, hMax))
    print('검색 완료 ::::::: ')
    print('-----------------------------------------------------------------------------------------------------------------')

    # 코인 disparity 순으로 정렬 / 검색된 코인 insert
    sortedByDisparity = []
    for coin in coins['recommends']:
        print("asdasdasdas", useRecommendOPtion.name)
        coinName = list(coin.keys())[0]
        sortedByDisparity.append(
            {'name': coinName, 'disparity': coin[coinName]['disparity'], 'price': coin[coinName]['closing_price']})

        RCCoin = models.recommendList()
        RCCoin.coin_name = coinName
        RCCoin.catch_price = coin[coinName]['closing_price']
        RCCoin.option_name = useRecommendOPtion.name
        RCCoin.user_idx = active_user.idx
        db.add(RCCoin)

    sortedCoins = sorted(sortedByDisparity, key=lambda x: x['disparity'])
    print(sortedCoins)

    # 거래 가능 금액 가져오기
    money = bithumb.get_balance('BTC')[2] - bithumb.get_balance('BTC')[3]
    print('deposit ::::::: ',active_user.idx, money)
    print('-----------------------------------------------------------------------------------------------------------------')
    moneyPerCoin: float = 0

    # 코인당 거래할 금액 계산
    if buyOption.checkbox == 1:
        moneyPerCoin = buyOption.price_to_buy_method * 10000

    elif buyOption.checkbox == 2:
        moneyPerCoin = (money * buyOption.percent_to_buy_method) / 100

    print(
        f'moneyPerCoin: {moneyPerCoin}, money: {money}, percent: {buyOption.percent_to_buy_method}')

    orders = ''
    orderList = []
    print(money)
    for coin in sortedCoins:
        try:
            # 구매 안하는 사유
            if coinCount >= int(accountOption.price_count):
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

            print(coinCount, accountOption.price_count, coin['name'])

            orders = ''

            print(coin)

            # 지정 호가 계산
            # ask = askingPrice.askingPrice(int(float(coin['price'])))
            # coin_ask_price = float(coin['price']) + (buyOption.callmoney_to_buy_method * ask)
            # coin_ask_price = (round(coin_ask_price,4))
            splitBuy = moneyPerCoin * 1

            if buyOption.callmoney_to_buy_method > 0:
                ask = f'+{buyOption.callmoney_to_buy_method}'
            else:
                ask = str(buyOption.callmoney_to_buy_method)

            coin_ask_price = askingPrice.ASK_PRICE(f"{coin['name']}", ask, 'buy')
            print('coin_ask_price ::::::: ', coin_ask_price)
            fee = bithumb.get_trading_fee(coin['name'])
            payment = float(splitBuy * (1 - fee))
            splitUnit = round(payment / (float(coin_ask_price)), 4)
            print('주문코인 정보 ::: ::: ', coin['name'], round(float(coin_ask_price), 2), round(splitUnit, 4), 'KRW')
            print("예수금", splitBuy)
            print("수수료 제외 매수 금액", payment)
            # 주문
            order = bithumb.buy_limit_order(
                coin['name'], round(float(coin_ask_price), 2), round(splitUnit, 4), 'KRW')
            print("order ::: :::",order)

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
        order_coin.cancel_time = (datetime.datetime.now(
        ) + datetime.timedelta(seconds=accountOption.buy_cancle_time))
        order_coin.user_idx = active_user.idx
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
        possession_coin.cancel_time = (datetime.datetime.now(
        ) + datetime.timedelta(seconds=accountOption.buy_cancle_time))
        possession_coin.macd_chart = macdOption.chart_term
        possession_coin.disparity_chart = disparityOption.chart_term
        possession_coin.optionName = useRecommendOPtion.name
        possession_coin.trailingstop_flag = 0
        possession_coin.max = possession_coin.price
        possession_coin.user_idx = active_user.idx
        db.add(possession_coin)

    try:
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()

    with open("./buyLog", "a") as file:
        file.write(
            f'{datetime.datetime.now()}------------------------------------------------------------------')
        for buyCoin in sortedCoins:
            file.write(str(buyCoin) + '\n')
        file.close()

    now2 = datetime.datetime.now()
    print(now2-now1)
