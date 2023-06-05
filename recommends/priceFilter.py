import pandas as pd

# 가격 정보, 가격 조건 받아 조건에 맞는 코인 리턴
def priceRecommend(nowstamp, coinList, dfList, lowPrice, highPrice):
    print(type(lowPrice), type(highPrice))
    priceL = []
    print(len(coinList), len(dfList), lowPrice, highPrice)
    lowPrice = int(lowPrice)

    time = nowstamp - (5 * 60)
    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] > time]

    for coin in coinList:
        print(coin)
        df3 = df2.loc[df['coin_name'] == coin]

        if len(df3) != 0 and df3.iloc[-1]['Close'] > float(lowPrice) and df3.iloc[-1]['Close'] < float(highPrice):
            if len(df3) == 0:
                continue

    print(len(priceL), 'price List =================================================================')

    return priceL
