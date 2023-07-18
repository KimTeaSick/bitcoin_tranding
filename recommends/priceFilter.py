import pandas as pd

# 가격 정보, 가격 조건 받아 조건에 맞는 코인 리턴
def priceRecommend(nowstamp, coinList, dfList, lowPrice, highPrice):
    print('-----------------------------------------------------------------------------------------------------------')
    print('price start ::::::: ')

    price_list = []
    price_value = []
    print(len(coinList), len(dfList), lowPrice, highPrice)

    lowPrice = int(lowPrice)

    time = nowstamp - (5 * 60)
    df = pd.DataFrame(dfList)
    time_satisfied_df = df.loc[df['S_time'] > time]

    for coin in coinList:
        matching_coin_name_df = time_satisfied_df.loc[df['coin_name'] == coin]

        if len(matching_coin_name_df) != 0 and matching_coin_name_df.iloc[-1]['Close'] > float(lowPrice) and matching_coin_name_df.iloc[-1]['Close'] < float(highPrice):
            price_list.append(coin)
            price_value.append({'coin_name':coin, 'price': matching_coin_name_df.iloc[-1]['Close']})

    print('price end ::::::: ',len(price_list))
    print('-----------------------------------------------------------------------------------------------------------')
    return price_list, price_value
