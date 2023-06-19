import pandas as pd

# 가격 정보, 가격 조건 받아 조건에 맞는 코인 리턴
def priceRecommend(nowstamp, coinList, dfList, lowPrice, highPrice):
    priceL = []
<<<<<<< HEAD
=======
    priceValue = []
    print(len(coinList), len(dfList), lowPrice, highPrice)

>>>>>>> 08c77ea9d59222493c5a61938b0a1e239955e07d
    lowPrice = int(lowPrice)

    time = nowstamp - (5 * 60)
    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] > time]

    for coin in coinList:
        df3 = df2.loc[df['coin_name'] == coin]

<<<<<<< HEAD
        if len(df3) == 0:
            continue
        if df3.iloc[-1]['Close'] > float(lowPrice) and df3.iloc[-1]['Close'] < float(highPrice):
=======
        if len(df3) != 0 and df3.iloc[-1]['Close'] > float(lowPrice) and df3.iloc[-1]['Close'] < float(highPrice):
>>>>>>> 08c77ea9d59222493c5a61938b0a1e239955e07d
            priceL.append(coin)
            priceValue.append({'coin_name':coin, 'price': df3.iloc[-1]['Close']})

    print(len(priceL), 'price List =================================================================')
    return priceL, priceValue
