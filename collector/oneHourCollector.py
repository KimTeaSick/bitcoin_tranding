import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import threading
import pandas as pd

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

currentPrice = []
macdCollector = []
fitCoins = []

now = datetime.datetime.now()
unix_timestamp = int(now.timestamp() /60 ) * 60 - 3600# 1시간전 변환

class MyThread(threading.Thread):
    def __init__(self, coinList):
        super().__init__()
        self.coinList = coinList

    def run(self):
        global currentPrice
        global macdCollector
        global unix_timestamp

        headers = {"accept": "application/json"}
        for coin in self.coinList:
            if coin.delflag == 1:
                continue
            url = f"https://api.bithumb.com/public/candlestick/{coin.coin_name}/1h"
            response = requests.get(url)
            data = response.json()["data"]

            time = datetime.datetime.now()

            try:
                # 데이터프레임 df 생성
                df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
                df2 = df['time']

                df['time'] = pd.to_datetime(df['time'], unit='ms') + datetime.timedelta(hours=9)

                # 빈 시간 0 채움
                df = df.set_index('time').resample('1H').asfreq()
                df = df.fillna(0)

                df3 = df[-100:]

                dt = df2[len(df2) -1] // 1000
                dt2 = datetime.datetime.fromtimestamp(dt)

                data2 = data[-1]
                data2.append(coin.coin_name)
                data2.append(dt2)


                # insert 할 내용 append
                if int(dt) == int(unix_timestamp):
                    currentPrice.append({'STime' : int(data2[0]/1000), 'Open': data2[1], 'Close': data2[2], 'High': data2[3], 'Low':data2[4], 'Volume': data2[5], 'coin_name': data2[6], 'time': data2[7]})

                else:
                    emptyCnt = int(((unix_timestamp - dt) / 60) /60)
                    currentPrice.append({'STime' : unix_timestamp, 'Open': data2[1], 'Close': data2[2], 'High': data2[3], 'Low': data2[4], 'Volume': data2[5], 'coin_name': data2[6], 'time': datetime.datetime.fromtimestamp(unix_timestamp), 'empty_count':emptyCnt})

                #df3.to_csv(f'./minCollector/csv/{coin.coin_name}{time.strftime("%d%H%M")}.csv', index=True)
                #print(currentPrice[-1])

            except Exception as e:
                print(e)

        print('thread done')

if __name__ == '__main__':
    now1 = datetime.datetime.now()
    print(now1)

    threads = []
    coinList = db.query(models.coinList).all()

    headers = {"accept": "application/json"}

    # 쓰레드 실행
    threads = []
    i = 0 
    for i in range(int(len(coinList)/10) + 1):
        j = i * 10
        t = MyThread(coinList[j:j+10])
        threads.append(t)
        i += 1

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(len(currentPrice))

    db.bulk_insert_mappings(models.coin1HPrice, currentPrice)
    db.commit()

    now2 = datetime.datetime.now()
    print(f'Running Time: {now2 - now1}')
