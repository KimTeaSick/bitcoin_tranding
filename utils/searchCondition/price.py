async def price_condition(p_condition, max_minute):
  if int(p_condition[1]['high_price']) == 0:
    print('high_price', p_condition[1]['high_price'])
    pass
  if 5 > max_minute:
    max_minute = 5
  return {'option': 'Price', 'low_price': p_condition[1]['low_price'], 'high_price': p_condition[1]['high_price']}, max_minute
