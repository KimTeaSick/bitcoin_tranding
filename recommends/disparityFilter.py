import pandas as pd
import numpy as np

# 이격도 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def disparityRecommend(nowstamp, coinList, dfList, chart_term, disparity_term, low_disparity, high_disparity):
    DisparityL = []

    # 기준시간 찾기
    times = int(chart_term[:-1])
    if chart_term[-1] == 'm':
        time = nowstamp - (int(times) * int(disparity_term) * 60)
    if chart_term[-1] == 'h':
        time = nowstamp - (int(times) * int(disparity_term) * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    df2 = df.loc[df['S_time'] >= time]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        df3 = df2.loc[df['coin_name'] == coin]
        df3.reset_index(drop=True, inplace=True)

        # 시간 범위 내 거래량 0인 코인 빼기
        vol = df3['Volume'].sum()
        if vol == 0.0:
            continue

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        df4 = df3[(len(df2) % times):]
        df4.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        new_df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

        # 이격도 계산
        avgP = new_df['Close'].mean()
        Recent = new_df['Close'].iloc[-1]
        disP = (Recent / avgP) * 100

        # 이격도 범위 비교
        if int(low_disparity) < disP and int(high_disparity) > disP :
                DisparityL.append(coin)

    print(DisparityL)
    return DisparityL