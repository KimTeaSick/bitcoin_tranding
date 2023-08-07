import math

def check_status(bit, buy_id, coin, unit):
  buyStatus = bit.get_order_completed(['bid', coin['coin'], buy_id, 'KRW'])
  print("check_status buyStatus", buyStatus)
  if buyStatus['data']['order_status'] == 'Completed':
    sell_unit =  unit + float(coin['unit'])
    sell_id = bit.sell_market_order(coin['coin'], sell_unit, "KRW")
    return sell_id[1]
  elif buyStatus['data']['order_status'] == 'Pending':
    check_status(bit, buy_id, coin, unit)


def one_doller_under_price_clean(bit, coin):
  try:
    print("one_doller_under_price_clean coin :: ::: ",coin)
    if float(coin['total']) <= 1000:
      unit = round(1500 / float(coin['nowprice']), 4)
      buy_id = bit.buy_market_order(coin['coin'], unit, "KRW")
      print("one dollar under price coin buy ::: ::: ", buy_id)
      sell_coin = check_status(bit, buy_id[2], coin, unit)
      return sell_coin
  except Exception as e:
    print("one_doller_under_price_clean Error ::: :::", e)