from BitThumbPrivate import BitThumbPrivate

bit = BitThumbPrivate()

def ASK_PRICE(coin, asking, trading_type):
    prices = []
    raw_ask_price_list = bit.bithumb.get_orderbook(coin, limit=11)
    ask_price_list = raw_ask_price_list['bids'] if trading_type == 'buy' else raw_ask_price_list['asks']

    for price in ask_price_list:
        prices.append(price['price'])

    print(prices)
    print(prices[round(len(prices)/2)])
    if asking[0] == '-':
        return prices[(round(len(prices)/2) + 1) - int(asking[1])]
    elif asking[0] == '+':
        return prices[(round(len(prices)/2) + 1) + int(asking[1])]

ask_price = ASK_PRICE('BTC_KRW','-1', 'buy')
print("ask_price :::: ",ask_price)
