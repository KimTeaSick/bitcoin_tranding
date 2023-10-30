def re_sell_coin_action(bithumb, sell_order):
  orderids = bithumb.sell_market_order(sell_order['coin'], float(sell_order['unit']), "KRW")
  return orderids

def sell_coin_action(bithumb, sell_order, askP):
  orderids = bithumb.sell_limit_order(sell_order['coin'], round(float(askP), 1), float(sell_order['unit']), "KRW")
  return orderids