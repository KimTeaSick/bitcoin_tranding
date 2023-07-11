from BitThumbPrivate import BitThumbPrivate

bit = BitThumbPrivate()

def ASK_PRICE(coin, ask):
    prices = []
    raw_ask_price_list = bit.bithumb.get_orderbook(coin, limit=11)
    ask_price_list = raw_ask_price_list['bids']
    for price in ask_price_list:
        prices.append(price['price'])

    print(prices)
    print(prices[round(len(prices)/2)])
    if ask[0] == '-':
        return prices[(round(len(prices)/2) + 1) - int(ask[1])]
    elif ask[0] == '+':
        return prices[(round(len(prices)/2) + 1) + int(ask[1])]

ask_price = ASK_PRICE('BTC_KRW','-1')
print("ask_price :::: ",ask_price)
