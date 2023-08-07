import websocket
import json
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import pandas as pd
from pybithumb import Bithumb
import datetime
import askingPrice

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()
 
# 빗썸 api 키 오
# secretKey = "c59e7f376201984d26224428649e42c7"
# connenctKey = "e2fee448690937ae2e8cd6dada5a183e"

# 빗썸 api 키 신
secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"

bithumb = Bithumb(connenctKey, secretKey)


trailingPercent = 0
sensingPercent = 0
accountOption = 0
askOption = 0

possessionCoin = {}
coinNames = []

minute = str(datetime.datetime.now().strftime('%M'))

def on_open(ws):
    print('WebSocket connection opened')
    # Send a subscribe message to the WebSocket
    subscribe_data = {
        "type": "transaction",
        "symbols": coinNames
    }
    ws.send(json.dumps(subscribe_data))


def on_message(ws, message):
    try:
        global possessionCoin
        global sensingPercent
        global trailingPercent
        global askOption
        global minute
        global accountOption

        data = eval(message)
        symbol = data['content']['list'][0]['symbol']
        price = float(data['content']['list'][0]['contPrice'])

        print("on_message data ::: ::: ", data)
        # 트레일링 스탑 시작
        if possessionCoin[symbol]['sensingPrice'] < price and possessionCoin[symbol]['trailingStop'] == 0:
            possessionCoin[symbol]['trailingStop'] = 1
        # 고가 비교
        if possessionCoin[symbol]['max'] < price:
            possessionCoin[symbol]['max'] = price
            possessionCoin[symbol]['trailingPrice'] = round(
                (price - ((trailingPercent / 100) * price)), 4)
        if possessionCoin[symbol]['trailingStop'] == 1:
            if possessionCoin[symbol]['trailingPrice'] > price:
                try:
                    status = db.query(models.possessionCoin).filter(
                        models.possessionCoin.coin == symbol[:-4]).first()
                    if status.status == 3 or status.status == 5:
                        print("매도 중 가격 ::: ::: ", price)
                        pass

                    else:
                        print(symbol, possessionCoin[symbol], price, '매도 ::: ::: ')
                        print('ask option ::: ::: ', askOption)
                        
                        askP = askingPrice.ASK_PRICE(
                            f'{symbol}_KRW', askOption, 'sell')

                        # 매도 주문
                        orderids = bithumb.sell_limit_order(
                            symbol[:-4], round(float(askP), 4), possessionCoin[symbol]['unit'], "KRW")
                        
                        print("order id ::: ::: ",orderids)

                        # 주문 테이블 저장
                        order_coin = models.orderCoin()
                        order_coin.coin = symbol[:-4]
                        order_coin.transaction_time = datetime.datetime.now()
                        order_coin.order_id = orderids[2]
                        order_coin.cancel_time = str(datetime.datetime.now() + datetime.timedelta(seconds=accountOption))
                        order_coin.sell_reason = 'trailing stop'

                        if status.status == 4:
                            status.status = 5
                            order_coin.status = 5
                        else:
                            status.status = 3
                            order_coin.status = 3

                        db.add(order_coin)
                        print(order_coin.cancel_time)

                        try:
                            db.commit()
                        except:
                            db.rollback()

                        with open("./sellLog", "a") as file:
                            file.write(
                                f'{datetime.datetime.now()}------------------------------------------------------------------\n')
                            file.write(
                                f"{'coin':symbol[:-4]}, reason: trailing stop" + '\n')
                            file.close()

                except Exception as e:
                    print(e)

        print(symbol, possessionCoin[symbol], price)

        # 보유 코인 확인
        nowMin = str(datetime.datetime.now().strftime('%M'))
        if minute != nowMin:
            minute = nowMin
            possession = db.query(models.possessionCoin).all()

            print(minute)
            for coin in possession:
                try:
                    coin.trailingstop_flag = possessionCoin[f'{coin.coin}_KRW']['trailingStop']
                    coin.max = possessionCoin[f'{coin.coin}_KRW']['max']
                except Exception as e:
                    print(e)

            try:
                db.commit()
            except:
                db.rollback()

            ws.close()
            start()

    except Exception as e:
        print(e)


def on_close(ws):
    print('WebSocket connection closed')


def on_error(ws, error):
    print('Error:', error)


def start():
    global coinNames
    global possessionCoin
    global coinList
    global sensingPercent
    global trailingPercent
    global askOption
    global accountOption
    active_users = db.query(models.USER_T).filter(models.USER_T.active == 1).all()
    for active_user in active_users:
        coinList = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == active_user.idx).all()
        useTradingOption = db.query(models.tradingOption).filter(
            models.tradingOption.idx == active_user.trading_option).first()
        accountOp = db.query(models.tradingAccountOption).filter(
            models.tradingAccountOption.idx == useTradingOption.idx).first()
        sellOption = db.query(models.tradingSellOption).filter(
            models.tradingSellOption.idx == useTradingOption.idx).first()
        autoStatus = db.query(models.autoTradingStatus).filter(
            models.autoTradingStatus.status == 1).first()
        accountOption = accountOp.sell_cancle_time
        if autoStatus == None:
            print('exit')
            print('자동 매매 정지')
            exit()
        sensingPercent = int(sellOption.trailing_start_percent)
        trailingPercent = int(sellOption.trailing_stop_percent)
        askOption = sellOption.trailing_order_call_price
        coinNames = []
        possessionCoin = {}

        for coin in coinList:
            print("coin ::: ::: ", coin.coin)
            if coin.status == 1:
                continue

            coinNames.append(f'{coin.coin}_KRW')
            trailingCoin = {'buyPrice': float(coin.price), 'sensingPrice': float(coin.price) + (float(coin.price) * (sensingPercent / 100)), 'trailingStop': coin.trailingstop_flag,
                            'max': float(coin.max), 'trailingPrice': float(coin.max) - (float(coin.max) * (trailingPercent / 100)), 'unit': float(coin.unit)}

            possessionCoin[f'{coin.coin}_KRW'] = trailingCoin

        if len(coinList) == 0:
            print('none coin')
            exit()

        print(possessionCoin)

        websocket_url = 'wss://pubwss.bithumb.com/pub/ws'
        ws = websocket.WebSocketApp(websocket_url,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_close=on_close,
                                    on_error=on_error)
        ws.run_forever()


start()
