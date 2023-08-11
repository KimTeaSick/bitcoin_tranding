from BitThumbPrivate import BitThumbPrivate

secretKey = "07c1879d34d18036405f1c4ae20d3023"
connenctKey = "9ae8ae53e7e0939722284added991d55"

bit = BitThumbPrivate(connenctKey, secretKey)

def ASK_PRICE(coin, asking, trading_type):
    ask_prices = []
    raw_ask_price_list = bit.bithumb.get_orderbook(coin, limit=11)
    ask_price_list = raw_ask_price_list['bids'] if trading_type == 'buy' else raw_ask_price_list['asks']
    for price in ask_price_list:
        ask_prices.append(price['price'])
    
    price = ask_prices[0]

    C_VALUE = askingPrice(price, int(asking[1]))

    if asking[0] == '-':
        return round(float(price) - C_VALUE, 4)
    elif asking[0] == '+':
        return round(float(price) + C_VALUE, 4)

# 호가 계산 함수
def askingPrice(price, asking=1):
    result: float = 0.0
    
    if price < 1:
        result = 0.0001
    elif price >= 1 and price < 10:
        result = 0.001
    elif price >= 10 and price < 100:
        result = 0.01
    elif price >= 100 and price < 1000:
        result = 0.1
    elif price >= 1000 and price < 5000:
        result = 1
    elif price >= 5000 and price < 10000:
        result = 5
    elif price >= 10000 and price < 50000:
        result = 10
    elif price >= 50000 and price < 100000:
        result = 50
    elif price >= 100000 and price < 500000:
        result = 100
    elif price >= 500000 and price < 1000000:
        result = 500
    elif price >= 1000000:
        result = 1000

    return round(result * asking, 4)
