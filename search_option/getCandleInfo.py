import requests

def getCandleInfo(item):
  coin = item["id"]
  term = item["term"]
  url = f"https://api.bithumb.com/public/candlestick/{coin}_KRW/{term}"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers).json()
  response = (response)
  return response