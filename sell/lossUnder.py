def LossUnderSell(coin, account_option):
  if coin['percent'] <= account_option.loss_cut_under_coin_specific_percent and account_option.loss == 2:
    return({'coin': coin['coin'], 'reason': 'loss cut under', 'unit': coin['unit'], 'close': coin['nowprice'],
            'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_under_call_price_specific_coin})
  if account_option.loss == 1:
    return({'coin': coin['coin'], 'reason': 'loss cut under', 'unit': coin['unit'], 'close': coin['nowprice'],
            'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_under_call_price_sell_all})