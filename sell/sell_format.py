def before_distinguish_coin_format(coin, response, nowPrice, ask):
  return {'coin': coin.coin, 'nowprice': response['data']['closing_price'], 'unit': coin.unit, 'buyPrice': coin.price, 'percent': (
      nowPrice / float(coin.total)) * 100 - 100, 'ask': ask, 'macd_chart': coin.macd_chart, 'disparity_chart': coin.disparity_chart, "total": coin.total }

def re_sale_coin_format(coin, sell_option):
  return ({'coin': coin['coin'], 'reason': 'resale', 'unit': coin['unit'], 'close': coin['nowprice'],
    'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': sell_option.call_money_to_sell_method})

def loss_cut_under_coin_format(coin, account_option):
  if coin['percent'] <= account_option.loss_cut_under_coin_specific_percent and account_option.loss == 2:
    return({'coin': coin['coin'], 'reason': 'loss cut under', 'unit': coin['unit'], 'close': coin['nowprice'],
            'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_under_call_price_specific_coin})
  if account_option.loss == 1:
    return({'coin': coin['coin'], 'reason': 'loss cut under', 'unit': coin['unit'], 'close': coin['nowprice'],
            'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': account_option.loss_cut_under_call_price_sell_all})
  
def price_drop_coin_format(coin, sell_option):
    return ({'coin': coin['coin'], 'reason': 'price under', 'unit': coin['unit'], 'close': coin['nowprice'],
        'buyPrice': coin['buyPrice'], 'ask': coin['ask'], 'askprice': sell_option.call_money_to_sell_method})

def insert_order_format(models, sell_order, orderids, transaction_time, cancel_time, idx, type ):
  order_coin = models.orderCoin()
  order_coin.coin = sell_order['coin']
  order_coin.status = 3 if type != "resale" else 5
  # order_coin.transaction_time = datetime.datetime.now()
  order_coin.transaction_time = transaction_time
  order_coin.order_id = orderids[2]
  # order_coin.cancel_time = (datetime.datetime.now() + datetime.timedelta(seconds=accountOtion.buy_cancle_time))
  order_coin.cancel_time = cancel_time
  order_coin.sell_reason = sell_order['reason']
  # order_coin.user_idx = active_user.idx
  order_coin.user_idx = idx
  return order_coin