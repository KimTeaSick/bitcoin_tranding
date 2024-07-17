import requests
import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import threading
import pandas as pd

# Initialize necessary variables
current_price = []
macd_collector = []
fit_coins = []

now = datetime.datetime.now()
unix_timestamp = int(now.timestamp() / 60) * 60 - 3600  # 1 hour ago

class CoinDataThread(threading.Thread):
    def __init__(self, coin_list):
        super().__init__()
        self.coin_list = coin_list

    def run(self):
        global current_price
        for coin in self.coin_list:
            if coin.delflag == 1:
                continue
            url = f"https://api.bithumb.com/public/candlestick/{coin.coin_name}/1h"
            response = requests.get(url)
            data = response.json()["data"]

            try:
                df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
                df['time'] = pd.to_datetime(df['time'], unit='ms') + datetime.timedelta(hours=9)
                df = df.set_index('time').resample('1H').asfreq().fillna(0)
                df2 = df['time']

                dt = df2.iloc[-1] // 1000
                dt2 = datetime.datetime.fromtimestamp(dt)
                last_data = data[-1] + [coin.coin_name, dt2]

                if int(dt) == int(unix_timestamp):
                    current_price.append({
                        'STime': int(last_data[0] / 1000),
                        'Open': last_data[1],
                        'Close': last_data[2],
                        'High': last_data[3],
                        'Low': last_data[4],
                        'Volume': last_data[5],
                        'coin_name': last_data[6],
                        'time': last_data[7]
                    })
                else:
                    empty_count = int(((unix_timestamp - dt) / 60) / 60)
                    current_price.append({
                        'STime': unix_timestamp,
                        'Open': last_data[1],
                        'Close': last_data[2],
                        'High': last_data[3],
                        'Low': last_data[4],
                        'Volume': last_data[5],
                        'coin_name': last_data[6],
                        'time': datetime.datetime.fromtimestamp(unix_timestamp),
                        'empty_count': empty_count
                    })

            except Exception as e:
                print(f"Error processing coin {coin.coin_name}: {e}")

        print('Thread done')

def get_coin_list():
    with SessionLocal() as db:
        return db.query(models.coinList).all()

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print(f"Start time: {start_time}")

    coin_list = get_coin_list()
    threads = []

    for i in range(0, len(coin_list), 10):
        thread = CoinDataThread(coin_list[i:i + 10])
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with SessionLocal() as db:
        db.bulk_insert_mappings(models.coin1HPrice, current_price)
        db.commit()

    end_time = datetime.datetime.now()
    print(f"Inserted {len(current_price)} records.")
    print(f"Running Time: {end_time - start_time}")
