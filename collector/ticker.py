import requests
import datetime
from database import SessionLocal
import models

def fetch_ticker_data():
    url = "https://api.bithumb.com/public/ticker/ALL_KRW"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()["data"]

def update_coin_prices(data, coins, unix_timestamp):
    current_list = []

    for ticker in data:
        coin_name = f'{ticker}_KRW'
        if coin_name in coins:
            try:
                current_list.append({
                    'S_time': unix_timestamp,
                    'Open': data[ticker]['opening_price'],
                    'Close': data[ticker]['closing_price'],
                    'High': data[ticker]['max_price'],
                    'Low': data[ticker]['min_price'],
                    'Volume': data[ticker]['units_traded'],
                    'coin_name': coin_name,
                    'time': datetime.datetime.fromtimestamp(unix_timestamp),
                    'Transaction_amount': data[ticker]['acc_trade_value_24H']
                })
            except Exception as e:
                print(f"Error processing {coin_name}: {e}")
    return current_list

def main():
    now1 = datetime.datetime.now()
    unix_timestamp = int(now1.timestamp() / 60) * 60

    with SessionLocal() as db:
        if now1.strftime("%H%M") == '0000':
            db.query(models.coinCurrentPrice).delete()

        coin_list = db.query(models.coinList).filter(models.coinList.delflag == 0).all()
        coins = {coin.coin_name for coin in coin_list}

        data = fetch_ticker_data()
        current_list = update_coin_prices(data, coins, unix_timestamp)

        # Using bulk insert or update
        db.bulk_update_mappings(models.coinCurrentPrice, current_list)
        db.commit()

    now2 = datetime.datetime.now()

    for tick in current_list:
        print(tick['coin_name'], tick['time'], tick['Close'], tick['Volume'], tick['Transaction_amount'])

    print(f"Running Time: {now2 - now1}")

if __name__ == '__main__':
    main()
