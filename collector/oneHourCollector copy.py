import requests
import datetime
from database import  SessionLocal
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
insertdata = []

now = datetime.datetime.now()
krTime = 60 * 9 * 60
class MyThread(threading.Thread):
    def __init__(self, coinList):
        super().__init__()
        self.coinList = coinList

    def run(self):
        try:
            global currentPrice
            global macdCollector
            global insertdata

            headers = {"accept": "application/json"}
            for coin in self.coinList:
                try:
                    if coin.delflag == 1:
                        continue
                    url = f"https://api.bithumb.com/public/candlestick/{coin.coin_name}/1h"
                    response = requests.get(url)
                    data = response.json()["data"]

                    time = datetime.datetime.now()
                    newtime = int(time.timestamp() / 3600) * 3600

                    print(data[-1][0]/1000, newtime, coin.coin_name)

                    for dat in data:
                        insertdata.append({'STime':dat[0]/1000, 'Open':dat[1], 'Close': dat[2], 'High':dat[3], 'Low':dat[4], 'Volume':dat[5], 'coin_name':coin.coin_name, 'time':datetime.datetime.fromtimestamp(dat[0]/1000)})
                except Exception as e:
                    print(e)

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

    print(insertdata)

    db.bulk_insert_mappings(models.coin1HPrice, insertdata)
    db.commit()

    now2 = datetime.datetime.now()
    print(f'Running Time: {now2 - now1}')
