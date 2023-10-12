def ReSaleSell(coin, sell_option):
  return ({'coin': coin['coin'], 'reason': 'resale', 'unit': coin['unit'], 'close': coin['nowprice'],
    'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': sell_option.call_money_to_sell_method})
