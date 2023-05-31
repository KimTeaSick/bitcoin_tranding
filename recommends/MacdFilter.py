import pandas as pd
import numpy as np

def MacdRecommend(nowstamp, coinList, dfList, chart_term, short_disparity, long_disparity, up_down):
    MacdL = []
    # 시간 데이터 부족으로 분단위 데이터 사용 중
    times = int(chart_term[:-1])

    if chart_term[-1] == 'm':
        time = nowstamp - (int(long_disparity) * (times) * 60)
    if chart_term[-1] == 'h':
        time = nowstamp - (int(long_disparity) * (times) * 3600)

    df = pd.DataFrame(dfList)

    df2 = df.loc[df['S_time'] > time]

    for coin in coinList:
        df3 = df2.loc[df['coin_name'] == coin]
        df3.reset_index(drop=True, inplace=True)

        df4 = df2[(len(df3) % times):]
        df4.reset_index(drop=True, inplace=True)

        vol = df2['Volume'].sum()
        if vol == 0.0:
            continue

        # 리스트를 times개씩 묶기
        new_df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

        # short EMA 계산
        emashort = new_df['Close'].ewm(span=int(short_disparity)).mean()
        # long EMA 계산
        emalong = new_df['Close'].ewm(span=int(long_disparity)).mean()
        # MACD 계산
        macd = emashort - emalong

        if up_down == 'up':
            if macd.iloc[-1] >= 0:
                MacdL.append(coin)

        if up_down == 'down':
            if macd.iloc[-1] <= 0:
                MacdL.append(coin)

    print(MacdL)
    return MacdL