import pandas as pd

# 거래대금 데이터, 범위 받아 조건에 맞는 코인 리턴 (수집기 수정후 수집기데이터 사용으로 수정예정)
def transactioAmountRecommend(nowstamp, coinList, dfList, chart_term, lowTransactionAmount, highTransactionAmount):
    transactionAmountL = []
    print(len(coinList), '거래대금77777777777777777777777777777777777777777777777777777777777777777777')

    if chart_term[-1] == 'm':
        time = nowstamp - (int(chart_term[:-1]) * 60)
    if chart_term[-1] == 'h':
        time = nowstamp - (int(chart_term[:-1]) * 3600)

    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] > time]

    for coin in coinList:
        if coin in coinList:
            df3 = df2.loc[df['coin_name'] == coin]
            if len(df3) != 0 and df3['Transaction_amount'].sum() > float(lowTransactionAmount) and df3['Transaction_amount'].sum() < float(highTransactionAmount):
                transactionAmountL.append(coin)

        else:
            pass

    print(len(transactionAmountL), '7777777777777777777777777777777777777777777777777777777777777777777777777777777')
    return transactionAmountL