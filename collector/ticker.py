import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

now1 = datetime.datetime.now()
url = "https://api.bithumb.com/public/ticker/ALL_KRW"
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
data = response.json()["data"]

now = datetime.datetime.now()
unix_timestamp = int(now.timestamp() / 60) * 60

if str(now.strftime("%H%M")) == '0000':
    db.query(models.coinCurrentPrice).delete()

coinList = db.query(models.coinList).filter(models.coinList.delflag == 0).all()
coins = []

for coin in coinList:
    coins.append(coin.coin_name)

currentList = []

for ticker in data:
    if f'{ticker}_KRW' in coins:
        try:
            currentList.append({'S_time': unix_timestamp, 'Open': data[ticker]['opening_price'], 'Close': data[ticker]['closing_price'], 'High': data[ticker]['max_price'], 'Low': data[ticker]['min_price'],
                                'Volume': data[ticker]['units_traded'], 'coin_name': ticker+'_KRW', 'time': datetime.datetime.fromtimestamp(unix_timestamp), 'Transaction_amount': data[ticker]['acc_trade_value_24H']})
        except Exception as e:
            print(e)
    else:
        tick = models.coinCurrentPrice()
        tick.coin_name = ticker+'_KRW'
        tick.S_time = unix_timestamp
        tick.Open = data[ticker]['opening_price']
        tick.Close = data[ticker]['closing_price']
        tick.High = data[ticker]['max_price']
        tick.Low = data[ticker]['min_price']
        tick.Volume = data[ticker]['units_traded']
        tick.time = datetime.datetime.fromtimestamp(unix_timestamp)
        tick.Transaction_amount = data[ticker]['acc_trade_value_24H']

        db.add(tick)

# db.bulk_update_mappings(models.coinCurrentPrice, currentList)

now2 = datetime.datetime.now()

for tick in currentList:
    print(tick['coin_name'], tick['time'], tick['Close'],
          tick['Volume'], tick['Transaction_amount'])

# db.commit()
print(now2 - now1)
