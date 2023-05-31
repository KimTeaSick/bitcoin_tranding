def priceRecommend(coinList, lowPrice, highPrice):
    priceL = []

    for coin in coinList:
        if coin['Close'] > float(lowPrice) and coin['Close'] < float(highPrice):
            priceL.append(coin['name'])

    return priceL
