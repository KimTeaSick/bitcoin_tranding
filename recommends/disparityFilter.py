import pandas as pd
import numpy as np
import datetime

# 이격도 조건, 현재시간, 데이터 가져와 조건에 맞는지 탐색
def disparityRecommend(nowstamp, coinList, dfList, chart_term, disparity_term, low_disparity, high_disparity):
    print('-----------------------------------------------------------------------------------------------------------')
    print('disparity start ::::::: ')
    print('disparity parameter ::::::: ', nowstamp, len(coinList), len(dfList), chart_term, disparity_term, low_disparity, high_disparity)
    print('before condition pass coins ::::::: ', len(coinList))
    fn_start = datetime.datetime.now()

    Disparity_list = []
    Disparity_value = []

    # 기준시간 찾기
    times = int(chart_term[:-1])
    time = nowstamp - (int(times) * int(disparity_term) * 60) if chart_term[-1] == 'm' else nowstamp - (int(times) * int(disparity_term) * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    df['date'] = pd.to_datetime(df['time'])

    time_satisfied_df = df.loc[df['S_time'] >= time]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
        matching_coin_name_df = time_satisfied_df.loc[df['coin_name'] == coin].copy()

        matching_coin_name_df.loc[:, 'time'] = pd.to_datetime(matching_coin_name_df['time'])
        matching_coin_name_df.index = pd.to_datetime(matching_coin_name_df['time'])
        matching_coin_name_df = matching_coin_name_df[~matching_coin_name_df.index.duplicated(keep='first')]
        matching_coin_name_df.reset_index(drop=True, inplace=True)

        matching_coin_name_df = matching_coin_name_df.set_index('time').resample('1H').asfreq()
        matching_coin_name_df = matching_coin_name_df.fillna(method='ffill')

        # 시간 범위 내 거래량 0인 코인 빼기
        vol = matching_coin_name_df['Volume'].sum()
        if vol == 0.0:
            continue

        # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
        tied_chart_term_df = matching_coin_name_df[(len(matching_coin_name_df) % times):]
        tied_chart_term_df.reset_index(drop=True, inplace=True)

        # 리스트를 times개씩 묶기
        tied_time_df = tied_chart_term_df.groupby(np.arange(len(tied_chart_term_df)) // times).mean(numeric_only=True)

        # 이격도 계산
        avgP = tied_time_df['Close'].mean()
        Recent = tied_time_df['Close'].iloc[-1]
        disP = (Recent / avgP) * 100

        # 이격도 범위 비교
        if int(low_disparity) < disP and int(high_disparity) > disP :
                Disparity_list.append(coin)
                Disparity_value.append({'coin_name': coin, 'disparity': disP})

    fn_end = datetime.datetime.now()
    print('disparity spend time ::::::: ', fn_end - fn_start)
    print('disparity end ::::::: ', len(Disparity_list))
    print('-----------------------------------------------------------------------------------------------------------')
    return Disparity_list, Disparity_value
