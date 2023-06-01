import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

now1 = datetime.datetime.now()
coinList = db.query(models.coinList).filter(models.coinList.delflag == 0).all()

for coin in coinList:
    try:
        now = datetime.datetime.now()

        # csv 파일 읽어오기
        try:
            current_time = now.strftime("%d%H%M")
            df = pd.read_csv(f"./csv/{coin.coin_name}{current_time}.csv")
        except:
            now = now - datetime.timedelta(minutes=1)
            current_time = now.strftime("%d%H%M")
            df = pd.read_csv(f"./csv/{coin.coin_name}{current_time}.csv")

        # 기간 지정
        end_date = pd.to_datetime(current_time)

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

        disparityMa = df["close"].rolling(window=12).mean()
        disparity = float(disparityMa) / float(df["close"][-1]) * 100

        print(disparityMa)

    except Exception as e:
        print(e, coin.coin_name)

now2 = datetime.datetime.now()
print(now2-now1)