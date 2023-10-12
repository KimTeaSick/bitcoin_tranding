import sell_format

def re_sell_coin_action(bithumb, sell_order, models):
  orderids = bithumb.sell_market_order(sell_order['coin'], float(sell_order['unit']), "KRW")
  sell_format.insert_order_format(orderids)
  return orderids

def sell_coin_action(bithumb, sell_order, askP, models):
  orderids = bithumb.sell_limit_order(sell_order['coin'], round(float(askP), 1), float(sell_order['unit']), "KRW")
  sell_format.insert_order_format(orderids)
  return orderids