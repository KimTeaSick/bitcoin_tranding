import pandas as pd
import numpy as np
import datetime

# 추세 조건, 현재 시간, 데이터 가져와 조건에 맞는지 탐색
def trendRecommend(nowstamp, coinList, dfList, chart_term, MASP, trend_term, trend_type, trend_reverse):
    TrendL = []
    print('trend', len(coinList))

    times = int(chart_term[:-1])

    # 기준시간 찾기
    if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 2) * times * 60)
    if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 2) * times * 60)

    if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 0:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 2) * times * 3600)
    if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 1:
        trdTime = nowstamp - ((int(trend_term) + int(MASP) + 2) * times * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] > trdTime]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        df3 = df2.loc[df2['coin_name'] == coin]
        df3.reset_index(drop=True, inplace=True)

        # 시간 범위 내 거래량 0인 코인 빼기
        vol = df3['Volume'].sum()
        if vol == 0.0:
            continue

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df4 = df3[(len(df3) % times):]
        df4.reset_index(drop=True, inplace=True)

        dflen = len(df4)
        # 리스트를 times개씩 묶기
        new_df = df4.groupby(np.arange(dflen) // times).mean(numeric_only=True)

        masp = new_df["Close"].rolling(window=int(MASP)).mean()
        masp.fillna(0)

        # 코인이 조건에 부합하는지 판단 
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
                    print(coin, z)
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

    print(len(TrendL), 'trend1111111111111111111111111111111111111111111111111111111111111111111')
    return TrendL