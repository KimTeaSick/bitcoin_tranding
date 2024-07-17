import requests
import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import threading
import pandas as pd

# Initialize necessary variables
current_price = []
error_count = 0
now = datetime.datetime.now()
unix_timestamp = int(now.timestamp() / 60) * 60 - 86400  # 24 hours ago

class CoinDataThread(threading.Thread):
    def __init__(self, coin_list):
        super().__init__()
        self.coin_list = coin_list

    def run(self):
        global current_price
        global error_count

        for coin in self.coin_list:
            if coin.delflag == 1:
                continue

            url = f"https://api.bithumb.com/public/candlestick/{coin.coin_name}/24h"
            response = requests.get(url)
            data = response.json().get("data", [])

            if not data:
                error_count += 1
                continue

            try:
                df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
                df['time'] = pd.to_datetime(df['time'], unit='ms') + datetime.timedelta(hours=9)
                dt = df['time'].iloc[-1] // 1000
                dt2 = datetime.datetime.fromtimestamp(dt)
                data2 = data[-1] + [coin.coin_name, dt2]

                if int(dt) == int(unix_timestamp):
                    current_price.append({
                        'STime': int(data2[0] / 1000),
                        'Open': data2[1],
                        'Close': data2[2],
                        'High': data2[3],
                        'Low': data2[4],
                        'Volume': data2[5],
                        'coin_name': data2[6],
                        'time': data2[7]
                    })
                else:
                    empty_count = int(((unix_timestamp - dt) / 60) / 1440)
                    current_price.append({
                        'STime': unix_timestamp,
                        'Open': data2[1],
                        'Close': data2[2],
                        'High': data2[3],
                        'Low': data2[4],
                        'Volume': data2[5],
                        'coin_name': data2[6],
                        'time': datetime.datetime.fromtimestamp(unix_timestamp),
                        'empty_count': empty_count
                    })
                print(current_price[-1])

            except Exception as e:
                print(f"Error processing coin {coin.coin_name}: {e}")
                error_count += 1

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
        db.bulk_insert_mappings(models.coin1DPrice, current_price)
        db.commit()

    end_time = datetime.datetime.now()
    print(f"Inserted {len(current_price)} records.")
    print(f"Running Time: {end_time - start_time}")
    print(f"Error count: {error_count}")
