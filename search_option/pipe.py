def Price_value_pipe(value):
  return_value = [{}]
  return_coin = []
  for coin in value:
    return_value[0][str(coin[0]).replace("_KRW", "")] = {'Close':coin[1]}
    return_coin.append(str(coin[0]).replace("_KRW", ""))
  return return_coin, return_value