import sys 
sys.path.append("/Users/josephkim/Desktop/bitcoin_trading_back")

from BitThumbPrivate import BitThumbPrivate
from sqlalchemy.orm import Session
from database import SessionLocal
from sql import *
import datetime
import models 

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class SearchFn():
  def __init__(self):
    self.bit = BitThumbPrivate()

  async def insertOption(self, item):
        try:
          print(item)
          opName = ''
          search_option = models.searchOption()
          price_option = models.PriceOption()
          transactionAmount_option = models.TransactionAmountOption()
          MASP_option = models.MASPOption()
          disparity_option = models.DisparityOption()
          trend_option = models.TrendOption()
          MACD_option = models.MACDOption()

          for i in item:
              if i[0] == 'Name':
                opName = i[1]
              if i[0] == 'Price':
                price_option.flag = i[1]['flag']
                price_option.low_price = i[1]['low_price']
                price_option.high_price = i[1]['high_price']
                price_option.name = opName
                db.add(price_option)
              if i[0] == 'TransactionAmount':
                transactionAmount_option.flag = i[1]['flag']
                transactionAmount_option.chart_term = i[1]['chart_term']
                transactionAmount_option.low_transaction_amount = i[1]['low_transaction_amount']
                transactionAmount_option.high_transaction_amount = i[1]['high_transaction_amount']
                transactionAmount_option.name = opName
                db.add(transactionAmount_option)
              if i[0] == 'MASP':
                MASP_option.flag = i[1]['flag']
                MASP_option.chart_term = i[1]['chart_term']
                MASP_option.first_disparity = i[1]['first_disparity']
                MASP_option.comparison = i[1]['comparison']
                MASP_option.second_disparity = i[1]['second_disparity']
                MASP_option.name = opName
                db.add(MASP_option)
              if i[0] == 'Disparity':
                disparity_option.flag = i[1]['flag']
                disparity_option.chart_term = i[1]['chart_term']
                disparity_option.disparity_term = i[1]['disparity_term']
                disparity_option.low_disparity = i[1]['low_disparity']
                disparity_option.high_disparity = i[1]['high_disparity']
                disparity_option.name = opName
                db.add(disparity_option)
              if i[0] == 'Trend':
                trend_option.flag = i[1]['flag']
                trend_option.chart_term = i[1]['chart_term']
                trend_option.MASP = i[1]['MASP']
                trend_option.trend_term = i[1]['trend_term']
                trend_option.trend_type = i[1]['trend_type']
                trend_option.trend_reverse = i[1]['trend_reverse']
                trend_option.name = opName
                db.add(trend_option)
              if i[0] == 'MACD':
                MACD_option.flag = i[1]['flag']
                MACD_option.chart_term = i[1]['chart_term']
                MACD_option.short_disparity = i[1]['short_disparity']
                MACD_option.long_disparity = i[1]['long_disparity']
                MACD_option.up_down = i[1]['up_down']
                MACD_option.signal = i[1]['signal']
                MACD_option.name = opName
                db.add(MACD_option)

          search_option.name = opName
          search_option.Price = opName
          search_option.Transaction_amount = opName
          search_option.MASP = opName
          search_option.Disparity = opName
          search_option.Trend = opName
          search_option.MACD = opName
          search_option.Create_date = datetime.datetime.now()
          search_option.used = 0
          db.add(search_option)
          try:
            db.commit()
            return 'Insert sucess'
          except Exception as e:
            db.rollback()
            print("db.rollback()", e)
            return 444
        except Exception as e:
          print(e)
          return 444

  async def optionList(self):
    try:
      optionL = db.query(models.searchOption).all()
      options = []
      for option in optionL:
        if option.Update_date == None:
          option.Update_date = "-"
        else:
          option.Update_date = option.Update_date[0:19]
        options.append(
          {'Name': option.name, 'Create_date': option.Create_date[0:19], 'Update_date': option.Update_date, 'used': option.used})
      return options
    except Exception as e:
      print("optionList Error :::: ", e)
      self.bit.mysql.Insert(insertLog, [e])
      db.rollback()
      return 444
    
  async def optionDetail(self, item):
      try:
          print(item)
          now1 = datetime.datetime.now()
          optionL = db.query(models.searchOption).filter(
              models.searchOption.name == item.option).first()
          pri = db.query(models.PriceOption).filter(
              models.PriceOption.name == optionL.Price).first()
          tra = db.query(models.TransactionAmountOption).filter(
              models.TransactionAmountOption.name == optionL.Transaction_amount).first()
          mas = db.query(models.MASPOption).filter(
              models.MASPOption.name == optionL.MASP).first()
          dis = db.query(models.DisparityOption).filter(
              models.DisparityOption.name == optionL.Disparity).first()
          trd = db.query(models.TrendOption).filter(
              models.TrendOption.name == optionL.Trend).first()
          mac = db.query(models.MACDOption).filter(
              models.MACDOption.name == optionL.MACD).first()
          now2 = datetime.datetime.now()
          print(now2-now1)
          return {optionL.name: {
                                "Price": {"low_price": pri.low_price, "high_price": pri.high_price, "flag": pri.flag},
                                "TransactionAmount": {"chart_term": tra.chart_term, "low_transaction_amount": tra.low_transaction_amount, "high_transaction_amount": tra.high_transaction_amount, "flag": tra.flag},
                                "MASP": {"chart_term": mas.chart_term, "first_disparity": mas.first_disparity, "comparison": mas.comparison, "second_disparity": mas.second_disparity, "flag": mas.flag},
                                "Trend": {"chart_term": trd.chart_term, "MASP": trd.MASP, "trend_term": trd.trend_term, "trend_type": trd.trend_type, "trend_reverse": trd.trend_reverse, "flag": trd.flag},
                                "Disparity": {"chart_term": dis.chart_term, "disparity_term": dis.disparity_term, "low_disparity": dis.low_disparity, "high_disparity": dis.high_disparity, "flag": dis.flag},
                                "MACD": {"chart_term": mac.chart_term, "short_disparity": mac.short_disparity, "long_disparity": mac.long_disparity, "up_down": mac.up_down, "flag": mac.flag, "signal": mac.signal}}}
      except Exception as e:
          print("optionList Error :::: ", e)
          self.bit.mysql.Insert(insertLog, [e])
          db.rollback()
          return 444
  async def updateOption(self, item):
      opName = ''
      for i in item:
          if i[0] == 'Name':
              opName = i[1]
          if i[0] == 'Price':
              low_price = i[1]['low_price']
              high_price = i[1]['high_price']
              PriFlag = i[1]['flag']
          if i[0] == 'TransactionAmount':
              low_transaction_amount = i[1]['low_transaction_amount']
              high_transaction_amount = i[1]['high_transaction_amount']
              Trachart_term = i[1]['chart_term']
              TraFlag = i[1]['flag']
          if i[0] == 'MASP':
              Schart_term = i[1]['chart_term']
              first_disparity = i[1]['first_disparity']
              comparison = i[1]['comparison']
              second_disparity = i[1]['second_disparity']
              MasFlag = i[1]['flag']
          if i[0] == 'Disparity':
              Dchart_term = i[1]['chart_term']
              disparity_term = i[1]['disparity_term']
              low_disparity = i[1]['low_disparity']
              high_disparity = i[1]['high_disparity']
              DisFlag = i[1]['flag']
          if i[0] == 'Trend':
              Tchart_term = i[1]['chart_term']
              MASP = i[1]['MASP']
              trend_term = i[1]['trend_term']
              trend_type = i[1]['trend_type']
              trend_reverse = i[1]['trend_reverse']
              TrdFlag = i[1]['flag']
          if i[0] == 'MACD':
              Cchart_term = i[1]['chart_term']
              short_disparity = i[1]['short_disparity']
              long_disparity = i[1]['long_disparity']
              signal = i[1]['signal']
              up_down = i[1]['up_down']
              MacFlag = i[1]['flag']
      optionL = db.query(models.searchOption).filter(
          models.searchOption.name == opName).first()
      pri = db.query(models.PriceOption).filter(
          models.PriceOption.name == optionL.Price).first()
      tra = db.query(models.TransactionAmountOption).filter(
          models.TransactionAmountOption.name == optionL.Transaction_amount).first()
      mas = db.query(models.MASPOption).filter(
          models.MASPOption.name == optionL.MASP).first()
      dis = db.query(models.DisparityOption).filter(
          models.DisparityOption.name == optionL.Disparity).first()
      trd = db.query(models.TrendOption).filter(
          models.TrendOption.name == optionL.Trend).first()
      mac = db.query(models.MACDOption).filter(
          models.MACDOption.name == optionL.MACD).first()
      pri.low_price = low_price
      pri.high_price = high_price
      pri.flag = PriFlag
      tra.chart_term = Trachart_term
      tra.low_transaction_amount = low_transaction_amount
      tra.high_transaction_amount = high_transaction_amount
      tra.flag = TraFlag
      mas.chart_term = Schart_term
      mas.first_disparity = first_disparity
      mas.comparison = comparison
      mas.second_disparity = second_disparity
      mas.flag = MasFlag
      dis.chart_term = Dchart_term
      dis.disparity_term = disparity_term
      dis.low_disparity = low_disparity
      dis.high_disparity = high_disparity
      dis.flag = DisFlag
      trd.chart_term = Tchart_term
      trd.MASP = MASP
      trd.trend_term = trend_term
      trd.trend_type = trend_type
      trd.trend_reverse = trend_reverse
      trd.flag = TrdFlag
      mac.chart_term = Cchart_term
      mac.short_disparity = short_disparity
      mac.long_disparity = long_disparity
      mac.signal = signal
      mac.up_down = up_down
      mac.flag = MacFlag
      optionL.Update_date = datetime.datetime.now()
      try:
          db.commit()
          print('commit')
      except:
          self.bit.mysql.Insert(insertLog, [e])
          db.rollback()
          print('rollback')
      return 'Insert sucess'
  async def deleteOption(self, item):
      try:
          optionL = db.query(models.searchOption).filter(
              models.searchOption.name == item.option).first()
          db.query(models.PriceOption).filter(
              models.PriceOption.name == item.option).delete()
          db.query(models.TransactionAmountOption).filter(
              models.TransactionAmountOption.name == item.option).delete()
          db.query(models.MASPOption).filter(
              models.MASPOption.name == item.option).delete()
          db.query(models.DisparityOption).filter(
              models.DisparityOption.name == item.option).delete()
          db.query(models.TrendOption).filter(
              models.TrendOption.name == item.option).delete()
          db.query(models.MACDOption).filter(
              models.MACDOption.name == item.option).delete()
          db.query(models.searchOption).filter(
              models.searchOption.name == item.option).delete()
          try:
              db.commit()
          except Exception as e:
              print(e)
              self.bit.mysql.Insert(insertLog, [e])
              db.rollback()
          return 'delete sucess'
      except Exception as e:
          print(e)
  async def useOption(self, item):
      try:
          print("useOption :::::", item)
          useOption = db.query(models.searchOption).filter(
              models.searchOption.name == item.option).first()
          print("useOption :::::", useOption.name)
          optionL = db.query(models.searchOption).filter(
              models.searchOption.used == 1).all()
          print("optionL :::::", optionL)
          for option in optionL:
              option.used = 0
          useOption.used = 1
          useOption.Update_date = datetime.datetime.now()
          db.commit()
          print("success :::::")
          return 200
      except Exception as e:
          print("fail :::::", e)
          db.rollback()
          return 444