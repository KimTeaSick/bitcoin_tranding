from .getBitcoinInfo import getBitcoinInfo
from .pushCoinName import pushCoinName

def price(option):
  returnList = []
  data = getBitcoinInfo('ALL')
  coinList = pushCoinName(data)
  for coin in coinList:
    coinPrice = float(coin['closing_price'])
    if coinPrice > float(option['low_price']) and coinPrice < float(option['high_price']):
      returnList.append(coin)
  return returnList
