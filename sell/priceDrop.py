def PriceDropSell(coin, sell_option):
  print("---------------------------------------------------------------------------------------------------------")
  print("PriceDrop Start ::: ::: ", coin)
  if coin['percent'] <= (- sell_option.down_percent_to_price_condition):
    return ({'coin': coin['coin'], 'reason': 'price under', 'unit': coin['unit'], 'close': coin['nowprice'],
        'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': sell_option.call_money_to_sell_method})
  pass
  print("PriceDrop End ::: ::: ")
  print("---------------------------------------------------------------------------------------------------------")