from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import pandas as pd
import models
from sqlalchemy import between

now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

# 1시간 전 데이터 ~ 최신 데이터 찾아서 dataframe 변환
now = str(datetime.datetime.now() - datetime.timedelta(hours=1))
findidx = now[:-10]
coinList = db.query(model.coinList).all()
find30m = db.query(model.coinPrice1M).filter(model.coinPrice1M.time.like(f'{findidx}%')).first()
performanceList = db.query(model.coinPrice1M).filter(model.coinPrice1M.idx > find30m.idx).all()

dfList = []

for performance in performanceList:
    dfList.append({'coin_name': performance.coin_name, 'S_time': performance.S_time, 'time': performance.time, 'Open': performance.Open, 'Close': performance.Close, 'High': performance.High, 'Low': performance.Low,
                   'Avg_price': performance.Avg_price, 'Transaction_amount': performance.Transaction_amount, 'Volume': performance.Volume, 'Disparity': performance.Disparity, 'Ask_price': performance.Ask_price})

df = pd.DataFrame(dfList)

bulkList = []

for coin in coinList:
    df2 = df.loc[df['coin_name'] == coin.coin_name]
    if len(df2) == 0:
        continue

    avgPrice = df2['Close'].mean()
    minPrice = df2['Close'].min()
    openPrice = df2['Close'].iloc[0]
    closePrice = df2['Close'].iloc[-1]
    maxPrice = df2['Close'].max()
    transaction_amount = df2['Transaction_amount'].sum()
    volume = df2['Volume'].sum()
    disparity = avgPrice / closePrice * 100

    #print(avgPrice, minPrice, openPrice, closePrice, maxPrice, disparity)

    bulkList.append({'coin_name': coin.coin_name, 'S_time': performance.S_time, 'time': performance.time, 'Open': openPrice, 'Close': closePrice, 'High': maxPrice, 'Low': minPrice,
                     'Avg_price': avgPrice, 'Transaction_amount': transaction_amount, 'Volume': volume, 'Disparity': disparity, 'Ask_price': 0})

#df = pd.DataFrame(oneMinList)

print(bulkList)
db.bulk_insert_mappings(model.coinPrice1H, bulkList)
db.commit()

now2 = datetime.datetime.now()
print(now2 - now1)
