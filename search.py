import json
import recommend
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import datetime
import asyncio
import requests
import askingPrice

url = 'http://192.168.10.43:8888'

now1 = datetime.datetime.now()
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()


# 사용 db 가져오기 
possessionCoins = db.query(models.possessionCoin).all()
useRecommendOPtion = db.query(models.searchOption).filter(models.searchOption.used == 1).first()
useTradingOption = db.query(models.tradingOption).filter(models.tradingOption.used == 1).first()

coinCount = len(possessionCoins)

# 매수 조건
accountOtion = db.query(models.tradingAccountOption).filter(models.tradingAccountOption.name == useTradingOption.name).first()
buyOtion = db.query(models.tradingBuyOption).filter(models.tradingBuyOption.name == useTradingOption.name).first()

async def priceSearch():
  # 검색 조건
  priceOtion = db.query(models.PriceOption).filter(models.PriceOption.name == useRecommendOPtion.name).first()
  transactionAmountOption = db.query(models.TransactionAmountOption).filter(models.TransactionAmountOption.name == useRecommendOPtion.name).first()
  maspOtion = db.query(models.MASPOption).filter(models.MASPOption.name == useRecommendOPtion.name).first()
  trendOption = db.query(models.TrendOption).filter(models.TrendOption.name == useRecommendOPtion.name).first()
  disparityOtion = db.query(models.DisparityOption).filter(models.DisparityOption.name == useRecommendOPtion.name).first()
  macdOption = db.query(models.MACDOption).filter(models.MACDOption.name == useRecommendOPtion.name).first()

  # 검색
  mMax:int = 0
  hMax:int = 0
  options: list = []

  if priceOtion.flag == 1:
      if priceOtion.high_price != 0:
          if 5 > mMax:
              mMax = 5

          options.append({'option': 'Price', 'low_price': priceOtion.low_price, 'high_price': priceOtion.high_price})

  if transactionAmountOption.flag == 1:
      if transactionAmountOption.high_transaction_amount != 0:
          if transactionAmountOption.chart_term[-1] == 'm' and int(transactionAmountOption.chart_term[:-1]) > mMax:
              mMax = int(transactionAmountOption.chart_term[:-1])

          if transactionAmountOption.chart_term[-1] == 'h' and int(transactionAmountOption.chart_term[:-1]) > hMax:
              hMax = int(transactionAmountOption.chart_term[:-1])

      options.append({'option':'TransactionAmount', 'chart_term':transactionAmountOption.chart_term, 'low_transaction_amount':transactionAmountOption.low_transaction_amount, 'high_transaction_amount':transactionAmountOption.high_transaction_amount})

  if maspOtion.flag == 1:
      if maspOtion.first_disparity != 0 and maspOtion.second_disparity != 0:
          print('first_disparity: ', maspOtion.first_disparity, 'second_disparity: ', maspOtion.second_disparity)

          if maspOtion.chart_term[-1] == 'm' and (maspOtion.first_disparity * int(maspOtion.chart_term[:-1])) > mMax:
              mMax = maspOtion.first_disparity * int(maspOtion.chart_term[:-1])
          if maspOtion.chart_term[-1] == 'm' and (maspOtion.second_disparity * int(maspOtion.chart_term[:-1])) > mMax:
              mMax = maspOtion.second_disparity * int(maspOtion.chart_term[:-1])

          if maspOtion.chart_term[-1] == 'h' and (maspOtion.first_disparity * int(maspOtion.chart_term[:-1])) > hMax:
              hMax = (maspOtion.first_disparity) * int(maspOtion.chart_term[:-1])
          if maspOtion.chart_term[-1] == 'h' and (maspOtion.second_disparity * int(maspOtion.chart_term[:-1])) > hMax:
              hMax = (maspOtion.second_disparity) * int(maspOtion.chart_term[:-1])

          options.append({'option': 'MASP', 'chart_term': maspOtion.chart_term, 'first_disparity': maspOtion.first_disparity, 'second_disparity': maspOtion.second_disparity, 'comparison': maspOtion.comparison})

  if disparityOtion.flag == 1:
      if disparityOtion.chart_term != 0:
          if disparityOtion.chart_term[-1] == 'm' and (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1])) > mMax:
              mMax = (disparityOtion.disparity_term * disparityOtion.chart_term[:-1])

          if disparityOtion.chart_term[-1] == 'h' and (disparityOtion.disparity_term * int(disparityOtion.chart_term[:-1])) > hMax:
              hMax = (disparityOtion.disparity_term * disparityOtion.chart_term[:-1])

          options.append({'option':'Disparity', 'chart_term': disparityOtion.chart_term, 'disparity_term':disparityOtion.disparity_term, 'low_disparity': disparityOtion.low_disparity, 'high_disparity': disparityOtion.high_disparity})


  if trendOption.flag == 1:
      if trendOption.trend_term != 0 and trendOption.MASP != 0:
          if trendOption.chart_term[-1] == 'm' and ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1])) > mMax:
              mMax = ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1]))

          if trendOption.chart_term[-1] == 'h' and ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1])) > hMax:
              hMax = ((trendOption.trend_term + 2 + trendOption.MASP) * int(trendOption.chart_term[:-1]))

          options.append({'option':'Trend', 'chart_term': trendOption.chart_term, 'trend_term': trendOption.trend_term, 'trend_type': trendOption.trend_type, 'trend_reverse': trendOption.trend_reverse, "MASP": trendOption.MASP})

  if macdOption.flag == 1:
      if macdOption.short_disparity != 0 and macdOption.long_disparity != 0:

          if macdOption.chart_term[-1] == 'm' and ((macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])) > mMax:
              mMax = (macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])

          if macdOption.chart_term[-1] == 'h' and ((macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])) > hMax:
              hMax = (macdOption.long_disparity * 2 + macdOption.signal) * int(macdOption.chart_term[:-1])

          options.append({'option':'MACD', 'chart_term':macdOption.chart_term, 'short_disparity':macdOption.short_disparity, 'long_disparity':macdOption.long_disparity,'signal':macdOption.signal, 'up_down':macdOption.up_down})

  print(options)
  print(f'mMax: {mMax}, hMax: {hMax}')

  # 검색 코인 receive
  coins = asyncio.run(recommendCoins(options, mMax, hMax))
  print('----------------------------------------------------------------------------------검색 완료')