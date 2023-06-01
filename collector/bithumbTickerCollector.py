import websocket
import json
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import pandas as pd

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

coinList = db.query(models.coinList).all()
coinNames = []
for coin in coinList:
    coinNames.append(coin.coin_name)

# 시간 홀수 짝수 판별
now = datetime.datetime.now().strftime("%H%M")
if (int(now) % 2) == 0:
    minOddEven = 'even'
else:
    minOddEven = 'odd'

oddColector = []
evenCollector = []

def on_open(ws):
    print('WebSocket connection opened')
    # Send a subscribe message to the WebSocket
    subscribe_data = {
    "type" : "transaction", 
    "symbols" : coinNames
    }
    ws.send(json.dumps(subscribe_data))

def on_message(ws, message):
    try:
        global minOddEven
        global oddColector
        global evenCollector
        global coinNames

        now = datetime.datetime.now().strftime("%H%M")

        data = eval(message)
        #print(f"코인명: {data['content']['symbol']}, 시가: {data['content']['openPrice']}, 종가:{data['content']['closePrice']}, 고가:{data['content']['highPrice']}, 저가:{data['content']['lowPrice']}, 시간{data['content']['time']}")
        oddEven = int(now) % 2

        # 홀수 짝수 분 데이터 append
        if oddEven == 1:
            for content in data['content']['list']:
                oddColector.append(content)
        if oddEven == 0:
            for content in data['content']['list']:
                evenCollector.append(content)

        if minOddEven == 'even' and (int(now) % 2) == 1:
            #print(evenCollector, 'even min ----------------------------------------------------------------------------------------------------')
            minOddEven = 'odd'
            # db 저장 함수 실행
            collectNinsert(evenCollector, coinNames)

            evenCollector = []

        if minOddEven == 'odd' and (int(now) % 2) == 0:
            #print(oddColector, 'even min ----------------------------------------------------------------------------------------------------')
            minOddEven = 'even'
            # db 저장 함수 시행
            collectNinsert(oddColector, coinNames)

            oddColector = []
    except Exception as e:
        print(e)


def on_close(ws):
    print('WebSocket connection closed')

def on_error(ws, error):
    print('Error:', error)

def collectNinsert(collector, coins):
    now1 = datetime.datetime.now()
    df = pd.DataFrame(collector)

    current = db.query(models.coinCurrentPrice).all()

    bulkinsert = []

    for coin in current:
        df2 = df.loc[df['symbol'] == coin.coin_name]
        transactionCnt = len(df2)
        now = datetime.datetime.now()
        unix_timestamp = int(now.timestamp() /60) * 60

        if transactionCnt == 0:
            #bulkinsert.append({'coin_name': coin.coin_name, 'S_time': unix_timestamp, 'time': datetime.datetime.fromtimestamp(unix_timestamp), 'Open': coin.Open, 'Close': coin.Close, 'High': coin.High, 'Low': coin.Low, 'Avg_price': 0, 'Transaction_amount': 0, 'Volume': 0, 'Disparity': 0, 'Ask_price': 0})
            pass

        else:
            df2 = df2.astype({'contPrice':'float', 'contQty':'float', 'contAmt':'float'})
            avgPrice = df2['contPrice'].mean()
            minPrice = df2['contPrice'].min()
            openPrice = df2['contPrice'].iloc[0]
            closePrice = df2['contPrice'].iloc[-1]
            maxPrice = df2['contPrice'].max()
            transaction_amount = df2['contAmt'].sum()
            volume = df2['contQty'].sum()
            disparity = avgPrice / closePrice * 100

            print(f'시가:{openPrice}, 종가:{closePrice}, 고가:{maxPrice}, 저가:{minPrice}, 평균가:{avgPrice}, 심볼:{coin.coin_name}')

            bulkinsert.append({'coin_name': coin.coin_name, 'S_time': unix_timestamp, 'time': datetime.datetime.fromtimestamp(unix_timestamp), 'Open': openPrice, 'Close': closePrice, 'High': maxPrice, 'Low': minPrice, 
                               'Avg_price': avgPrice, 'Transaction_amount': transaction_amount, 'Volume': volume, 'Disparity': disparity, 'Ask_price': 0})

    '''
    try:
        #db.bulk_insert_mappings(models.coinPrice1M, bulkinsert)
        db.commit()

    except Exception as e:
        print(e)
        db.rollback()'''

    #for row in bulkinsert:
        #print(row)
    print(len(bulkinsert))

    now2 = datetime.datetime.now()
    print(now2 - now1, '-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

websocket_url = 'wss://pubwss.bithumb.com/pub/ws'
ws = websocket.WebSocketApp(websocket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close,
                            on_error=on_error)

ws.run_forever()
