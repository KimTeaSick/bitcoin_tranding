from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from routers.user.userApi import user
import psutil
from pybithumb import Bithumb
 

class TestFn():
  def signTradeFn(self, order, bit):
    order_desc= [order.type, order.coin, order.order_id, 'KRW']
    orderStatus = bit.bithumb.get_order_completed(order_desc)
    return orderStatus
  
  def cancleTradeFn(self):
    for proc in psutil.process_iter():
      try:
        # 프로세스 이름, PID값 가져오기
        processName = proc.name()
        processID = proc.pid
        print(processName , ' - ', processID)
        if processName == "ProcessName":
            parent_pid = processID  #PID
            parent = psutil.Process(parent_pid) # PID 찾기
            parent.kill() 
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
        pass

  def testFn(self):
    bit = Bithumb("aeda5f9da2474b1a374db964c23c0f1c", "e9f80d26e7a60ba7e076161325eb2704")
    coinList = bit.get_balance('ALL')
    coinList = coinList['data']
    coinTotalList = dict.items(coinList)
    totalList = []
    myCoinList = []
    return_list = []
    for item in coinTotalList:
        if ('total_' in str(item[0])):
            totalList.append(item)
    for item in totalList:
        if (float(item[1]) >= 0.0001):
            if item[0] != 'total_krw':
                if item[0] != 'total_bm':
                    coin_name = item[0]
                    myCoinList.append(coin_name[6:])
    for coin in myCoinList:
      raw_coin_info = bit.get_info_ticker(coin)
      coin_info= raw_coin_info["data"]
      coin_name = coin_info["order_currency"]
      coin_avg_price = coin_info["average_price"]
      coin_unit = coin_info["units_traded"]
      coin_total_price = float(coin_unit) * float(coin_avg_price)
      if coin_total_price >= 1000:
        return_list.append({ "name": coin_name, "price":coin_avg_price, "unit":coin_unit, "total": coin_total_price })
    return return_list
  
  async def getBithumbCoinList(self):
        try:
            row_coin_list = await self.mysql.Select(get_bithumb_coin_list_sql)
            coin_list = changer.BITHUMB_COIN_LIST(row_coin_list)
            with open('/data/4season/nc_bit_trading/src/variables/coin_list.json', 'w', encoding="utf-8") as make_file:
                json.dump(coin_list, make_file, ensure_ascii=False, indent="\t")
            return coin_list
        except Exception as e:
            print("Error :::: ", e)
            return