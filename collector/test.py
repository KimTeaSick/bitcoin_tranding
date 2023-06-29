import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import threading
import pandas as pd
import time

'''
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

coinList = db.query(models.coinList).all()

for coin in coinList:
    try:




        macd_short, macd_long, macd_signal=12,26,9 #기본값
        df["MACD_short"]=df["종가"].ewm(span=macd_short).mean()
        df["MACD_long"]=df["종가"].ewm(span=macd_long).mean()
        df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
        df["MACD_signal"]=df["MACD"].ewm(span=macd_signal).mean()  
        df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)
        df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)
    except Exception as e:
        print(e)'''


data=requests.get('https://api.bithumb.com/public/candlestick/BTC_KRW/24h')
data=data.json()
data=data.get("data")
df=pd.DataFrame(data)

df.rename(columns={0:'time',1:"시가", 2:"종가", 3:"고가",4:"저가",5:"거래량"}, inplace=True)
df.sort_values("time", inplace=True)
df=df[['time',"시가", "종가", "고가","저가","거래량"]].astype("float")
df.reset_index(drop=True, inplace=True)
df["date"]=df["time"].apply(lambda x:time.strftime('%Y-%m-%d %H:%M', time.localtime(x/1000)))

macd_short, macd_long, macd_signal=15,60,9
df["MACD_short"]=df["종가"].ewm(span=macd_short).mean()
df["MACD_long"]=df["종가"].ewm(span=macd_long).mean()
df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
df["MACD_signal"]=df["MACD"].ewm(span=macd_signal).mean()  
df["MACD_oscillator"]=df.apply(lambda x:(x["MACD"]-x["MACD_signal"]), axis=1)
df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)
print(df)
