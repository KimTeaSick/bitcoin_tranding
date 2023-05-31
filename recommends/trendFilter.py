import pandas as pd
import numpy as np
import datetime

def trendRecommend(nowstamp, coinList, dfList, chart_term, MASP, trend_term, trend_type, trend_reverse):
    TrendL = []

    times = int(chart_term[:-1])

    if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)

    if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)

    df = pd.DataFrame(dfList)
    print((int(trend_term) + int(MASP) + 1) * times)
    print(datetime.datetime.utcfromtimestamp(trdTime))
    df2 = df.loc[df['S_time'] > trdTime]

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

        masp = new_df["Close"].rolling(window=int(MASP)).mean()
        masp.fillna(0)

        z = 0
        if trend_type == 'up_trend' and int(trend_reverse) == 0:
            for i in range(int(MASP), len(new_df)):

                if float(masp[i]) == 0:
                    continue

                if float(masp[i]) > float(masp[i-1]):
                    z += 1
                else:
                    z = 0

                if z == int(trend_term):
                    TrendL.append(coin)

        if trend_type == 'down_trend' and int(trend_reverse) == 0:
            for i in range(int(MASP), len(new_df)):
                if float(masp[i]) == 0:
                    continue

                if float(masp[i]) < float(masp[i-1]):
                    z += 1
                else:
                    z = 0

                if z == int(trend_term):
                    TrendL.append(coin)

        if trend_type == 'up_trend' and int(trend_reverse) == 1:
            for i in range(int(MASP), len(new_df)):
                if float(masp[i]) == 0:
                    continue

                if z == int(trend_term):
                    if float(masp[i]) < float(masp[i-1]):
                        TrendL.append(coin)

                if float(masp[i]) > float(masp[i-1]):
                    z += 1
                else:
                    z = 0

        if trend_type == 'down_trend' and int(trend_reverse) == 1:
            for i in range(int(MASP), len(new_df)):
                if z == int(trend_term):
                    if float(masp[i]) > float(masp[i-1]):
                        TrendL.append(coin)

                if float(masp[i]) < float(masp[i-1]):
                    z += 1
                else:
                    z = 0
    print(TrendL)
    return TrendL