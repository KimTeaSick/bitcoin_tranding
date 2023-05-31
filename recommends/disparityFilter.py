import pandas as pd
import numpy as np

def disparityRecommend(nowstamp, coinList, dfList, chart_term, disparity_term, low_disparity, high_disparity):
    DisparityL = []

    times = int(chart_term[:-1])
    if chart_term[-1] == 'm':
        time = nowstamp - (int(times) * int(disparity_term) * 60)
    if chart_term[-1] == 'h':
        time = nowstamp - (int(times) * int(disparity_term) * 3600)

    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] >= time]

    for coin in coinList:
        df3 = df2.loc[df['coin_name'] == coin]
        df3.reset_index(drop=True, inplace=True)

        vol = df3['Volume'].sum()
        if vol == 0.0:
            continue

        df4 = df3[(len(df2) % times):]
        df4.reset_index(drop=True, inplace=True)

        dflen = len(df4)
        # 리스트를 times개씩 묶기
        new_df = df4.groupby(np.arange(dflen) // times).mean(numeric_only=True)

        avgP = new_df['Close'].mean()
        Recent = new_df['Close'].iloc[-1]
        disP = (Recent / avgP) * 100

        if int(low_disparity) < disP:
            if int(high_disparity) > disP :
                DisparityL.append(coin)

    print(DisparityL)
    return DisparityL