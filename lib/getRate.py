import json
import requests

def getBitCoinList(coin):  # 코인 리스트, 코인 정보 가져오기
  url = f"https://api.bithumb.com/public/ticker/{coin}_KRW"
  headers = {"accept": "application/json"}
  response = json.loads(requests.get(url, headers=headers).text)
  return response

def checkAccount(bit):  # 보유 예수금 목록
    try:
        response = bit.get_balance('BTC')
        KRW = response[2]
        return KRW
    except Exception as e:
        print("checkAccount Error :::: ", e)
        return 444

def myProperty(bit):
  coinList = get_my_coin_list(bit)
  list = []
  money = 0
  for i in coinList:
      coinInfo = getBitCoinList(str(i[0]).replace('total_', ""))
      if int(coinInfo['status']) == 5500:
          continue
      coinValue = float(
          coinInfo['data']['closing_price']) * round(float(i[1]), 4)
      list.append(coinValue)
  for index in range(len(list)):
      money += list[index]
  account = checkAccount(bit)
  money += account
  return money, account

def get_my_coin_list(bit):  # 현재 보유 코인 종류
  coinList = bit.get_balance('All')
  coinList = coinList['data']
  coinTotalList = dict.items(coinList)
  totalList = []
  myCoinList = []
  for item in coinTotalList:
      if ('total_' in str(item[0])):
          totalList.append(item)
  for item in totalList:
      if (float(item[1]) >= 0.0001):
          if item[0] != 'total_krw':
              if item[0] != 'total_bm':
                  myCoinList.append(item)
  return myCoinList

def now_rate_fn(db, models, bit, idx):
    try:
        total_revenue = 0
        investment_amount = 0
        property_value = 0
        coin_list = get_my_coin_list(bit)
        possession_coin_list = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == idx).all()
        for possession_coin in possession_coin_list:   
            coin_info = getBitCoinList(possession_coin.coin)
            if int(coin_info['status']) == 5500:
                continue
            buy_at_coin_value = float(possession_coin.price) * round(float(possession_coin.unit), 4)
            now_coin_value = float(coin_info['data']['closing_price']) * round(float(possession_coin.unit), 4)
            revenue = now_coin_value - buy_at_coin_value
            investment_amount += buy_at_coin_value
            total_revenue += revenue
        for coin in coin_list:
            coin_name = str(coin[0]).replace('total_', '')
            coin_info = getBitCoinList(coin_name)
            if int(coin_info['status']) == 5500:
                continue
            coin_value = float(coin_info['data']['closing_price']) * round(float(coin[1]), 4)
            property_value += coin_value
        now_balance = myProperty(bit)[0]
        rate = round((total_revenue / property_value) * 100, 2)
        print("rate ",rate)
        return rate
    except Exception as e:
        print(e)