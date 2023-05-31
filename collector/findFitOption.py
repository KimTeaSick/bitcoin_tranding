import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from multiprocessing import Process
import pandas as pd
import json

now1 = datetime.datetime.now()

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

headers = {"accept": "application/json"}

url = f"https://api.bithumb.com/public/candlestick/BTC_KRW/1m"
response = requests.get(url)

data = response.json()['data']

df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)

options = db.query(models.findOption).all()

for option in options:
    disparityVal = db.query(models.disparityOption).filter(models.disparityOption.disparity_idx == option.trends_idx).first()
    disparityMa = df["close"].rolling(window=int(disparityVal.disparity_value)).mean()[-1]
    disparity = float(disparityMa) / float(df["close"][-1]) * 100

    transactionAmount = float(df["close"][-1]) * float(df["volume"][-1])

    # 조건 검색
    if float(option.first_disparity) < disparity < float(option.second_disparity):
        if float(option.avg_volume) < float(df["volume"][-1]) and float(option.price) < float(df['close'][-1]) and float(option.transaction_amount) < transactionAmount:
            trend = float(df["close"][-(int(option.trends) + 1)])
            x = 0

            for i in range(int(option.trends), 0, -1):
                if trend < float(df["close"][-int(option.trends)]):
                    x += 1
                    trend = float(df["close"][-int(option.trends)])
            if x == int(option.trends):
                print("BTC_KRW")

now3 = datetime.datetime.now()

print(now3-now1)

#print(option.name, option.first_disparity, option.second_disparity, option.trends, option.trends_idx, option.avg_volume, option.transaction_amount, option.price)

'''
# 데이터프레임 df 생성
df = pd.DataFrame(data, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)

# 12일 EMA 계산
ema12 = df['close'].ewm(span=12).mean()
# 26일 EMA 계산
ema26 = df['close'].ewm(span=26).mean()
# MACD 계산
macd = ema12 - ema26

# Signal line 계산
signal_line = macd.ewm(span=9).mean()

# MACD histogram 계산
macd_histogram = macd - signal_line
'''
