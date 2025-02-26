from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from sqlalchemy.orm import Session
from database import SessionLocal
from returnValue import changer
from utils import insertLog, getDate
from sqld import *
import subprocess
import datetime
import models 
import psutil


try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

class TradeFn():
  async def insertTradingOPtion(self, item):
        try:
            print(item.name)
            trading_option = models.tradingOption()
            trading_account_option = models.tradingAccountOption()
            trading_buy_option = models.tradingBuyOption()
            trading_sell_option = models.tradingSellOption()

            trading_option.name = item.name
            trading_option.insert_time = datetime.datetime.now()
            trading_option.update_time = "-"
            trading_option.used = 0
            print(item.name)
            db.add(trading_option)
            db.flush()
            print(trading_option.idx)

            for i in item:
                if i[0] == 'account':
                    trading_account_option.idx = trading_option.idx
                    trading_account_option.price_count = i[1]['price_count']
                    trading_account_option.loss_cut_under_percent = i[1]['loss_cut_under_percent']
                    trading_account_option.loss = i[1]['loss']
                    trading_account_option.loss_cut_under_call_price_sell_all = i[
                        1]['loss_cut_under_call_price_sell_all']
                    trading_account_option.loss_cut_under_coin_specific_percent = opName = i[
                        1]['loss_cut_under_coin_specific_percent']
                    trading_account_option.loss_cut_under_call_price_specific_coin = i[
                        1]['loss_cut_under_call_price_specific_coin']
                    trading_account_option.loss_cut_over_percent = i[1]['loss_cut_over_percent']
                    trading_account_option.gain = i[1]['gain']
                    trading_account_option.loss_cut_over_call_price_sell_all = i[
                        1]['loss_cut_over_call_price_sell_all']
                    trading_account_option.loss_cut_over_coin_specific_percent = i[
                        1]['loss_cut_over_coin_specific_percent']
                    trading_account_option.loss_cut_over_call_price_specific_coin = i[
                        1]['loss_cut_over_call_price_specific_coin']
                    trading_account_option.buy_cancle_time = i[1]['buy_cancle_time']
                    trading_account_option.sell_cancle_time = i[1]['sell_cancle_time']

                    db.add(trading_account_option)

                if i[0] == 'buy':
                    trading_buy_option.idx = trading_option.idx
                    trading_buy_option.percent_to_buy_method = i[1]['percent_to_buy_method']
                    trading_buy_option.price_to_buy_method = i[1]['price_to_buy_method']
                    trading_buy_option.callmoney_to_buy_method = i[1]['callmoney_to_buy_method']
                    trading_buy_option.checkbox = i[1]['checkbox']
                    db.add(trading_buy_option)

                if i[0] == 'sell':
                    trading_sell_option.idx = trading_option.idx
                    trading_sell_option.upper_percent_to_price_condition = i[
                        1]['upper_percent_to_price_condition']
                    trading_sell_option.down_percent_to_price_condition = i[
                        1]['down_percent_to_price_condition']
                    trading_sell_option.disparity_for_upper_case = i[1]['disparity_for_upper_case']
                    trading_sell_option.upper_percent_to_disparity_condition = i[
                        1]['upper_percent_to_disparity_condition']
                    trading_sell_option.disparity_for_down_case = i[1]['disparity_for_down_case']
                    trading_sell_option.down_percent_to_disparity_condition = i[
                        1]['down_percent_to_disparity_condition']
                    trading_sell_option.call_money_to_sell_method = i[1]['call_money_to_sell_method']
                    trading_sell_option.percent_to_split_sell = i[1]['percent_to_split_sell']
                    trading_sell_option.shot_MACD_value = i[1]['shot_MACD_value']
                    trading_sell_option.long_MACD_value = i[1]['long_MACD_value']
                    trading_sell_option.MACD_signal_value = i[1]['MACD_signal_value']

                    trading_sell_option.trailing_start_percent = i[1]['trailing_start_percent']
                    trading_sell_option.trailing_stop_percent = i[1]['trailing_stop_percent']
                    trading_sell_option.trailing_order_call_price = i[1]['trailing_order_call_price']
                    db.add(trading_sell_option)

            try:
                db.commit()
                return 'Insert sucess'

            except Exception as e:
                db.rollback()
                print("db.rollback()", e)
                insertLog.log(e)
                return 444

        except Exception as e:
            print(e)
            return 444

  async def tradingOptionList(self, idx):
      try:
          option_list = db.query(models.tradingOption).all()
          user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
          options = []
          for option in option_list:
              used = 0
              if user.trading_option == option.idx:
                used = 1
              options.append(
                  {'idx': option.idx, 'Name': option.name, 'Create_date': option.insert_time[:19], 'Update_date': option.update_time[:19], 'used': used})
              print(options)
          return options
      except Exception as e:
          print("tradingOptionListError :::: ", e)
          insertLog.log(e)
          db.rollback()
          return 444
      
  async def tradingOptionDetail(self, item):
      try:
          print(item)
          now1 = datetime.datetime.now()
          optionL = db.query(models.tradingOption).filter(
              models.tradingOption.idx == item.idx).first()
          accountL = db.query(models.tradingAccountOption).filter(
              models.tradingAccountOption.idx == item.idx).first()
          buyL = db.query(models.tradingBuyOption).filter(
              models.tradingBuyOption.idx == item.idx).first()
          sellL = db.query(models.tradingSellOption).filter(
              models.tradingSellOption.idx == item.idx).first()
          now2 = datetime.datetime.now()
          print(now2-now1)
          return {optionL.name: {
                                'idx':optionL.idx,
                                'account': {"price_count": accountL.price_count, "loss_cut_under_percent": accountL.loss_cut_under_percent, "loss_cut_under_call_price_sell_all": accountL.loss_cut_under_call_price_sell_all, "loss_cut_under_coin_specific_percent": accountL.loss_cut_under_coin_specific_percent, "loss_cut_under_call_price_specific_coin": accountL.loss_cut_under_call_price_specific_coin, "loss_cut_over_percent": accountL.loss_cut_over_percent, "loss_cut_over_call_price_sell_all": accountL.loss_cut_over_call_price_sell_all, "loss_cut_over_coin_specific_percent": accountL.loss_cut_over_coin_specific_percent, "loss_cut_over_call_price_specific_coin": accountL.loss_cut_over_call_price_specific_coin, "buy_cancle_time": accountL.buy_cancle_time, "sell_cancle_time": accountL.sell_cancle_time, "loss": accountL.loss, "gain": accountL.gain},
                                "buy": {"percent_to_buy_method": buyL.percent_to_buy_method, "price_to_buy_method": buyL.price_to_buy_method, "callmoney_to_buy_method": buyL.callmoney_to_buy_method, "checkbox": buyL.checkbox},
                                "sell": {"upper_percent_to_price_condition": sellL.upper_percent_to_price_condition, "down_percent_to_price_condition": sellL.down_percent_to_price_condition, "disparity_for_upper_case": sellL.disparity_for_upper_case, "upper_percent_to_disparity_condition": sellL.upper_percent_to_disparity_condition, "disparity_for_down_case": sellL.disparity_for_down_case, "down_percent_to_disparity_condition": sellL.down_percent_to_disparity_condition, "call_money_to_sell_method": sellL.call_money_to_sell_method, "percent_to_split_sell": sellL.percent_to_split_sell, "shot_MACD_value": sellL.shot_MACD_value, "long_MACD_value": sellL.long_MACD_value, "MACD_signal_value": sellL.MACD_signal_value, "trailing_start_percent": sellL.trailing_start_percent, "trailing_stop_percent": sellL.trailing_stop_percent, "trailing_order_call_price": sellL.trailing_order_call_price}
                                }}
      except Exception as e:
          print("tradingOptionListError :::: ", e)
          insertLog.log(e)
          db.rollback()
          return 444
      
  async def updateTradingOption(self, item):
      try:
          print("item.idx ::: ::: ", item.idx)
          for i in item:
              if i[0] == 'account':
                  price_count = i[1]['price_count']
                  loss_cut_under_percent = i[1]['loss_cut_under_percent']
                  loss = i[1]['loss']
                  loss_cut_under_call_price_sell_all = i[1]['loss_cut_under_call_price_sell_all']
                  loss_cut_under_coin_specific_percent = opName = i[
                      1]['loss_cut_under_coin_specific_percent']
                  loss_cut_under_call_price_specific_coin = i[1]['loss_cut_under_call_price_specific_coin']
                  loss_cut_over_percent = i[1]['loss_cut_over_percent']
                  gain = i[1]['gain']
                  loss_cut_over_call_price_sell_all = i[1]['loss_cut_over_call_price_sell_all']
                  loss_cut_over_coin_specific_percent = i[1]['loss_cut_over_coin_specific_percent']
                  loss_cut_over_call_price_specific_coin = i[1]['loss_cut_over_call_price_specific_coin']
                  buy_cancle_time = i[1]['buy_cancle_time']
                  sell_cancle_time = i[1]['sell_cancle_time']
              if i[0] == 'buy':
                  percent_to_buy_method = i[1]['percent_to_buy_method']
                  price_to_buy_method = i[1]['price_to_buy_method']
                  callmoney_to_buy_method = i[1]['callmoney_to_buy_method']
                  checkbox = i[1]['checkbox']
              if i[0] == 'sell':
                  upper_percent_to_price_condition = i[1]['upper_percent_to_price_condition']
                  down_percent_to_price_condition = i[1]['down_percent_to_price_condition']
                  disparity_for_upper_case = i[1]['disparity_for_upper_case']
                  upper_percent_to_disparity_condition = i[1]['upper_percent_to_disparity_condition']
                  disparity_for_down_case = i[1]['disparity_for_down_case']
                  down_percent_to_disparity_condition = i[1]['down_percent_to_disparity_condition']
                  call_money_to_sell_method = i[1]['call_money_to_sell_method']
                  percent_to_split_sell = i[1]['percent_to_split_sell']
                  shot_MACD_value = i[1]['shot_MACD_value']
                  long_MACD_value = i[1]['long_MACD_value']
                  MACD_signal_value = i[1]['MACD_signal_value']
                  trailing_start_percent = i[1]['trailing_start_percent']
                  trailing_stop_percent = i[1]['trailing_stop_percent']
                  trailing_order_call_price = i[1]['trailing_order_call_price']

          optionL = db.query(models.tradingOption).filter(
              models.tradingOption.idx == item.idx).first()
          accountL = db.query(models.tradingAccountOption).filter(
              models.tradingAccountOption.idx == item.idx).first()
          buyL = db.query(models.tradingBuyOption).filter(
              models.tradingBuyOption.idx == item.idx).first()
          sellL = db.query(models.tradingSellOption).filter(
              models.tradingSellOption.idx == item.idx).first()
          
          accountL.price_count = price_count
          accountL.loss_cut_under_percent = loss_cut_under_percent
          accountL.loss = loss
          accountL.loss_cut_under_call_price_sell_all = loss_cut_under_call_price_sell_all
          accountL.loss_cut_under_coin_specific_percent = loss_cut_under_coin_specific_percent
          accountL.loss_cut_under_call_price_specific_coin = loss_cut_under_call_price_specific_coin
          accountL.loss_cut_over_percent = loss_cut_over_percent
          accountL.gain = gain
          accountL.loss_cut_over_call_price_sell_all = loss_cut_over_call_price_sell_all
          accountL.loss_cut_over_coin_specific_percent = loss_cut_over_coin_specific_percent
          accountL.loss_cut_over_call_price_specific_coin = loss_cut_over_call_price_specific_coin
          accountL.buy_cancle_time = buy_cancle_time
          accountL.sell_cancle_time = sell_cancle_time
          buyL.percent_to_buy_method = percent_to_buy_method
          buyL.price_to_buy_method = price_to_buy_method
          buyL.callmoney_to_buy_method = callmoney_to_buy_method
          buyL.checkbox = checkbox
          sellL.upper_percent_to_price_condition = upper_percent_to_price_condition
          sellL.down_percent_to_price_condition = down_percent_to_price_condition
          sellL.disparity_for_upper_case = disparity_for_upper_case
          sellL.upper_percent_to_disparity_condition = upper_percent_to_disparity_condition
          sellL.disparity_for_down_case = disparity_for_down_case
          sellL.down_percent_to_disparity_condition = down_percent_to_disparity_condition
          sellL.call_money_to_sell_method = call_money_to_sell_method
          sellL.percent_to_split_sell = percent_to_split_sell
          sellL.shot_MACD_value = shot_MACD_value
          sellL.long_MACD_value = long_MACD_value
          sellL.MACD_signal_value = MACD_signal_value
          sellL.trailing_start_percent = trailing_start_percent
          sellL.trailing_stop_percent = trailing_stop_percent
          sellL.trailing_order_call_price = trailing_order_call_price
          optionL.update_time = datetime.datetime.now()

          try:
              db.commit()
              print('commit')
          except Exception as e:
              print("tradingOptionListError :::: ", e)
              insertLog.log(e)
              db.rollback()
              return 444
          return 'Insert sucess'
      except Exception as e:
          print("tradingOptionListError :::: ", e)
          insertLog.log(e)
          db.rollback()
          return 444
      
  async def deleteTradingOption(self, item):
      try:
          db.query(models.tradingOption).filter(
              models.tradingOption.idx == item.idx).delete()
          db.query(models.tradingAccountOption).filter(
              models.tradingAccountOption.idx == item.idx).delete()
          db.query(models.tradingBuyOption).filter(
              models.tradingBuyOption.idx == item.idx).delete()
          db.query(models.tradingSellOption).filter(
              models.tradingSellOption.idx == item.idx).delete()
          try:
              db.commit()
          except Exception as e:
              print(e)
              db.rollback()
          return 'delete sucess'
      except Exception as e:
          print("tradingOptionListError :::: ", e)
          insertLog.log(e)
          db.rollback()
          return 444
      
  async def useTradingOption(self, item, idx):
    try:
        print("item ::: ::: ",item)
        user = db.query(models.USER_T).filter(
            models.USER_T.idx == idx).first()
        user.trading_option = item.idx
        db.commit()
    except:
        db.rollback()

  async def getSearchPriceList(self, idx):
    try:
        returnValue = []
        searchList = db.query(models.recommendList).filter(models.recommendList.user_idx == idx).all()
        for coin in searchList:
            returnValue.append({'name': coin.coin_name, 'catch_price': coin.catch_price })
        return returnValue
    except Exception as e:
        db.rollback()
        insertLog.log(e)
        print("getSearchPriceList :::: ", e)
        return 444  
      
  async def getNowUseCondition(self, idx, bit):
      try:
          searchCondition = await bit.mysql.Select(findUseSearchCondition(idx))
          tradingCondition = await bit.mysql.Select(findUseTradingCondition(idx))
          searchOption = await bit.mysql.Select(useSearchOptionStatus(str(searchCondition[0][0])))
          tradingOption = await bit.mysql.Select(useTradingOptionStatus(str(tradingCondition[0][0])))
          searchOptionReturnValue = changer.SEARCH_CONDITION(searchOption)
          tradingOptionReturnValue = changer.TRADING_CONDITION(tradingOption)
          return {"searchOption": searchOptionReturnValue, "tradingOption": tradingOptionReturnValue}
      except Exception as e:
          print("tradingOptionListError :::: ", e)
          insertLog.log(e)
          return 444  
      
  async def getTradingHis(self, bit, idx):
      try:
          returnValue = []
          tradingHis = await bit.mysql.Select(getTradingHisSql(idx))  
          if (tradingHis != None):
              for his in tradingHis:
                  returnValue.append(changer.TRADING_LIST(his))
          return returnValue
      except:
          return 444  
  
  async def nowAutoStatusCheck(self, bit):
    try:
        status = await bit.mysql.Select(autoStatusCheck)
        return {"now_status": status[0][0]}
    except Exception as e:
        print("tradingOptionListError :::: ", e)
        insertLog.log(e)
        return 444
      
  async def getATOrderList(self, bit, idx):
    return_value = []
    raw_data = await bit.mysql.Select(getATOrderList(idx))
    if len(raw_data) == 0:
        return return_value
    else:
        for o_list in raw_data:
            return_value.append(changer.ATOrderList(o_list))
    return return_value
    
  async def controlAutoTrading(self, flag, bit, idx):
    try:
        user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
        if (flag == 1):
            user.active = 1
            user.start_date = str(datetime.datetime.now().replace())
            process = ['nohup', '/bin/python3', '/data/4season/trailingStop/main.py', str(idx), '&']
            subprocess.run(['/bin/python3', '/data/4season/bitcoin_trading_back/autoBuy.py'])
            subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, start_new_session=True)
        elif (flag == 0):
            orderList = db.query(models.orderCoin).filter(models.orderCoin.user_idx == user.idx).all()
            for order in orderList:
                Possession = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == user.idx).first()
                if order.status == 1:
                    order_desc = ['bid', order.coin, order.order_id, 'KRW']
                elif order.status == 3 or order.status == 5:
                    order_desc = ['ask', order.coin, order.order_id, 'KRW']
                cancel = bit.bithumb.cancel_order(order_desc)
                if cancel == True:
                    if order.status == 1:
                        db.delete(Possession)
                    elif order.status == 3 or order.status == 5:
                        Possession.status = 4
                    db.delete(order)
                    Possession.status = 0
            for proc in psutil.process_iter():
                try:
                    processCmdline = proc.cmdline()
                    print("proc ::: ::: ", processCmdline)
                    if len(processCmdline) >= 4:
                        print("proc ::: ::: ", processCmdline[1], "idx ::: :::", processCmdline[2])
                        if processCmdline[1] == '/data/4season/trailingStop/main.py' and processCmdline[2] == str(idx):
                            processID = proc.pid
                            autoTrading = psutil.Process(processID)
                            autoTrading.kill() 
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
                    pass
            user.start_date = "-"
            user.active = 0
        db.commit()        
        return 200
    except Exception as e:
        print("controlAutoTrading :::: ", e)
        db.rollback()
        return 444
    
  async def autoTradingOn(self, idx):
    try:
        user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
        user.active = 1
        user.start_date = str(datetime.datetime.now().replace())
        process = ['/bin/python3', '/data/4season/trailingStop/main.py', str(idx)]
        # process = f'/bin/python3 /data/4season/trailingStop/main.py {idx}'
        subprocess.run(['/bin/python3', '/data/4season/bitcoin_trading_back/_autoBuy.py', str(idx)], check=True)
        # subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, start_new_session=True)
        subprocess.Popen(process, stdout=subprocess.DEVNULL )
        db.commit()        
        return 200
    except subprocess.CalledProcessError as e:
        print("subprocess CalledProcessError ::: :::", e)
        db.rollback()
        raise
    except Exception as e:
        print("autoTradingOn Error :::: ", e)
        db.rollback()
        raise  
    
  async def autoTradingOff(self, bit, idx):
    try:
        user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
        order_list = db.query(models.orderCoin).filter(models.orderCoin.user_idx == user.idx).all()
        for order in order_list:
            possession_coin = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == user.idx).first()
            if order.status == 1:
                order_desc = ['bid', order.coin, order.order_id, 'KRW']
            elif order.status == 3 or order.status == 5:
                order_desc = ['ask', order.coin, order.order_id, 'KRW']
            cancel = bit.bithumb.cancel_order(order_desc)
            if cancel == True:
                if order.status == 1:
                    db.delete(possession_coin)
                elif order.status == 3 or order.status == 5:
                    possession_coin.status = 4
                db.delete(order)
                possession_coin.status = 0
        for proc in psutil.process_iter():
            try:
                processCmdline = proc.cmdline()
                print("proc ::: ::: ", processCmdline)
                if len(processCmdline) >= 3:
                    print("proc ::: ::: ", processCmdline[1], "idx ::: :::", processCmdline[2])
                    if processCmdline[1] == '/data/4season/trailingStop/main.py' and processCmdline[2] == str(idx):
                        processID = proc.pid
                        autoTrading = psutil.Process(processID)
                        autoTrading.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
                print("autoTradingOff psutil Error :::: ", e)
                db.rollback()
                raise 
        user.start_date = "-"
        user.active = 0
        db.commit()
        return 200
    except Exception as e:
        print("autoTradingOff Error :::: ", e)
        db.rollback()
        raise 

  def sellFn(self, bit, idx, item):
    try:
        if item.sellType == 1:
            orderId = bit.sellLimitOrder(item.coin, item.sellPrice, item.coinUnit)
        if item.sellType == 2:
            orderId = bit.sellMarketOrder(item.coin, item.coinUnit)
        print("orderId", orderId)
        transactionTime = getDate.getTransactionTime()
        cancleTime = getDate.getCancleTime(transactionTime, item.cancleTime)
        insertOrder = models.orderCoin()
        insertOrder.coin = item.coin
        insertOrder.status = 3
        insertOrder.transaction_time = transactionTime
        insertOrder.order_id = orderId[2]
        insertOrder.cancel_time = cancleTime
        insertOrder.sell_reason = "sell"
        insertOrder.user_idx = idx
        db.add(insertOrder)
        db.commit()
        return 200
    except Exception as e:
        print("sellFn Error :::: ", e)
        db.rollback()
