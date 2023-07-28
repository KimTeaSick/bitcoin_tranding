def LossOverSell(coin, account_option):
  if coin['percent'] >= account_option.loss_cut_over_coin_specific_percent and account_option.gain == 2:
    return ({'coin': coin['coin'], 'reason': 'loss cut over', 'unit': coin['unit'], 'close': coin['nowprice'],
             'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_over_call_price_specific_coin})
  if account_option.gain == 1:
    return ({'coin': coin['coin'], 'reason': 'loss cut over', 'unit': coin['unit'], 'close': coin['nowprice'],
             'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_over_call_price_sell_all})
    
  print('로스컷 오버 판매 완료')