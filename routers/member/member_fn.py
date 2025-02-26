from routers.member.returnValue import memberListReturnValue
import sql.memberSql as memSql
from dotenv import load_dotenv
import os
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
pwd = "/Users/josephkim/Desktop/bitcoin_trading_back" if IS_DEV == "True" else "/data/4season/bitcoin_trading_back"
import sys
sys.path.append(pwd) 
from routers.trade.trade_fn import TradeFn


class MemberFn():
  async def getMemberListFn(self, bit):
    returnValue = []
    RawMemberList = await bit.mysql.Select(memSql.getMemberListSql)
    for member in RawMemberList:
      data = memberListReturnValue(member)
      returnValue.append(data)
    return returnValue

  def controlTradingFn(self,bit, idx, status):
    TF = TradeFn()
    if status == 1:
      res = TF.autoTradingOn(idx)
    elif status == 0:
      res = TF.autoTradingOff(bit, idx)
    return res