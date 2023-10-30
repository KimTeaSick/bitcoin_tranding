import requests
import json

def getBitcoinInfo(coin):
  url = f'https://api.bithumb.com/public/ticker/{coin}_KRW'
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers).json()
  coin = response['data']
  return coin