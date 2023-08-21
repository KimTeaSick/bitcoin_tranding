from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from routers.user.userApi import user
import psutil
 

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