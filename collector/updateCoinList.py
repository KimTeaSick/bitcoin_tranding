import requests
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

url = "https://api.bithumb.com/public/ticker/ALL_KRW"

headers = {"accept": "application/json"}
response = requests.get(url)
data = response.json()["data"]

coinlist1 = []
for dat in data:
    dat += '_KRW'
    coinlist1.append(dat)

coinlist2 = []
coinList = db.query(model.coinList).all()
for coin in coinList:
    coinlist2.append(coin.coin_name)

coinlist3 = list(set(coinlist1) - set(coinlist2))
coinlist4 = list(set(coinlist2) - set(coinlist1))

for coin in coinList:
    if coin.coin_name in coinlist4:
        coin.delflag = 1

for coin in coinlist3:
    newCoin = model.coinList()
    newCoin.coin_name = coin
    newCoin.delflag = 0
    db.add(newCoin)

db.commit()