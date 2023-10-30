import os
from dotenv import load_dotenv
load_dotenv()
IS_DEV = os.environ.get('IS_DEV')
DEV_PWD = os.environ.get('DEV_PWD')
PRO_PWD = os.environ.get('PRO_PWD')
pwd = DEV_PWD if IS_DEV == "True" else PRO_PWD
import sys 
sys.path.append(pwd) 
import sell_format
import json
import askingPrice
import requests

def get_sell_list_cal(possession_coins):
  bithumbApi = 'https://api.bithumb.com/public/ticker/'
  headers = {"accept": "application/json"}
  possession: float = 0.0 # 보유 종목 총합 매수 단가
  nowWallet = 0.0 # 보유 종목 총합 현재가
  under_one_dollar = []
  isSell = [] # 매도 리스트
  resale = [] # 재 매도 리스트
  for coin in possession_coins:
    try:
      possession += float(coin.total)
      response = json.loads(requests.get(bithumbApi + coin.coin+'_KRW', headers=headers).text)
      nowPrice = float(response['data']['closing_price']) * float(coin.unit)
      ask = askingPrice.askingPrice(float(response['data']['closing_price']))
      if float(coin.total) != 0.0 or float(nowPrice) != 0.0:
        if float(coin.total) <= 1000:
          under_one_dollar.append(sell_format.before_distinguish_coin_format(coin, response, nowPrice, ask))
        elif coin.status == 4 and float(coin.total) >= 1000:
          resale.append(sell_format.before_distinguish_coin_format(coin, response, nowPrice, ask))
        else:
          isSell.append(sell_format.before_distinguish_coin_format(coin, response, nowPrice, ask))
      nowWallet += nowPrice
    except:
      continue
  return possession, nowWallet, isSell, resale, under_one_dollar

def get_max_chart_term_time(possession_coins, sellOption):
  chartMax = 0 
  for possession in possession_coins:
    macd_chart = int(possession.macd_chart[:-1])
    disparity_chart = int(possession.disparity_chart[:-1])
    chartMax = max(macd_chart, disparity_chart)
  max_time = 0
  disparity_upper_case = sellOption.disparity_for_upper_case * chartMax
  disparity_down_case = sellOption.disparity_for_down_case * chartMax
  long_macd_value = (sellOption.long_MACD_value + sellOption.MACD_signal_value + 1) * chartMax
  max_time = max(max_time, disparity_upper_case, disparity_down_case, long_macd_value)
  max_time += 10
  return max_time

def re_sale_list_cal(resale, sellOption):
  re_sale_list = []
  for sell in resale:
    re_sale_list.append(sell_format.re_sale_coin_format(sell, sellOption))
  return re_sale_list

def loss_cut_under_list_cal(isSell, rate_percent, account_option):
  loss_cut_under_list = []
  if float(rate_percent) <= -float(account_option.loss_cut_under_percent):
    for sell_coin in isSell:
      loss_cut_under_list.append(sell_format.loss_cut_under_coin_format(sell_coin, account_option))
  return loss_cut_under_list

def drop_down_coin_list_cal(isSell, sell_option):
  drop_down_coin_list = []
  for coin in isSell:
    if coin['percent'] <= (- sell_option.down_percent_to_price_condition):
      drop_down_coin_list.append(sell_format.price_drop_coin_format(coin, sell_option))
  return drop_down_coin_list