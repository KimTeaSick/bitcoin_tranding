from BitThumbPrivate import BitThumbPrivate

bit = BitThumbPrivate()


def ASK_PRICE(coin, asking, trading_type):
    prices = []
    raw_ask_price_list = bit.bithumb.get_orderbook(coin, limit=11)
    ask_price_list = raw_ask_price_list['bids'] if trading_type == 'buy' else raw_ask_price_list['asks']

    for price in ask_price_list:
        prices.append(price['price'])

    print(prices[round(len(prices)/2)])
    if asking[0] == '-':
        return prices[(round(len(prices)/2) + 1) - int(asking[1])]
    elif asking[0] == '+':
        return prices[(round(len(prices)/2) + 1) + int(asking[1])]


#ask_price = ASK_PRICE('BTC_KRW', '-1', 'buy')
#print("ask_price :::: ", ask_price)

# 호가 계산 함수 
def askingPrice(price):
    result:float = 0.0
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

    return result