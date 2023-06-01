# 가격 정보, 가격 조건 받아 조건에 맞는 코인 리턴
def priceRecommend(coinList, lowPrice, highPrice):
    priceL = []

    for coin in coinList:
        if coin['Close'] > float(lowPrice) and coin['Close'] < float(highPrice):
            priceL.append(coin['name'])

    return priceL
