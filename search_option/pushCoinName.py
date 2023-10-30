def pushCoinName(dict: dict):
  coinList = []
  for key, val in dict.items():
    if(type(val) == str): continue
    val["coin_name"] = key
    coinList.append(val)
  return coinList