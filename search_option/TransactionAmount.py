from .getBitcoinInfo import getBitcoinInfo
from .pushCoinName import pushCoinName

def TransactionAmountCondtion(coinList, option):
  returnList = []
  for coin in coinList:
    tradeValue = float(coin['acc_trade_value'])
    if tradeValue > float(option['low_transaction_amount']) and tradeValue < float(option['high_transaction_amount']):
      returnList.append(coin)
  return returnList


# def TransactionAmountCondtion(coin_list, low_limit, high_limit, bit):
#   return_coin =[]
#   for coin in coin_list:
#     item = {"id": str(coin).replace("_KRW", ""), "term": "1h"}
#     row_data = bit.getBitCoinList(item['id'])
#     data = row_data['data']
#     if float(data['acc_trade_value_24H']) > float(low_limit) and float(data['acc_trade_value_24H']) <= float(high_limit): pass
#     else: 
#       # return_coin[0][coin] = {'Close': coin_list[0][coin]['Close'], 'TA': data['acc_trade_value_24H']}
#       return_coin.append(str(coin).replace("_KRW", ""))
#   print("Transaction_amount_coondtion return_coin :::: ", return_coin)
#   return return_coin