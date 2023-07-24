import pandas as pd
import numpy as np
import datetime

# 추세 조건, 현재 시간, 데이터 가져와 조건에 맞는지 탐색
def trendRecommend(nowstamp, coinList, dfList, chart_term, MASP, trend_term, trend_type, trend_reverse):
    print('-----------------------------------------------------------------------------------------------------------')
    print('trend start ::::::: ')
    print('trend paramater ::::::: ', datetime.datetime.utcfromtimestamp(nowstamp), len(dfList), chart_term, MASP, trend_term, trend_type, trend_reverse)
    print('before condition pass coins ::::::: ', len(coinList))
    fn_start = datetime.datetime.now()
    Trend_list = []
    Trend_value = []

    times = int(chart_term[:-1])

    # 기준시간 찾기
    if chart_term[-1] == 'm':
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 60) if int(trend_reverse) == 0 else nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)
    if chart_term[-1] == 'h':
        trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 3600) if int(trend_reverse) == 0 else nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)

    # if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 0:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 60)
    # if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 0:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 60)
    # if chart_term[-1] == 'm' and trend_type == 'up_trend' and int(trend_reverse) == 1:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)
    # if chart_term[-1] == 'm' and trend_type == 'down_trend' and int(trend_reverse) == 1:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 60)

    # if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 0:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 3600)
    # if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 0:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP)) * times * 3600)
    # if chart_term[-1] == 'h' and trend_type == 'up_trend' and int(trend_reverse) == 1:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)
    # if chart_term[-1] == 'h' and trend_type == 'down_trend' and int(trend_reverse) == 1:
    #     trdTime = nowstamp - ((int(trend_term) + int(MASP) + 1) * times * 3600)

    # dataframe 생성 및 기준 시간 이후 데이터로 자르기
    df = pd.DataFrame(dfList)
    #df['date'] = pd.to_datetime(df['time'])
    #df['time'] = pd.to_datetime(df['time'])
    print((int(trend_term) + int(MASP) + 1) * times)

    time_satisfied_df = df.loc[df['S_time'] > trdTime]

    # 코인별로 순회하며 조건에 맞는지 찾기
    for coin in coinList:
      try:
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

        dflen = len(tied_chart_term_df)
        # 리스트를 times개씩 묶기
        tied_time_df = tied_chart_term_df.groupby(np.arange(dflen) // times).mean(numeric_only=True)

        masp = tied_time_df["Close"].rolling(window=int(MASP)).mean()
        masp.fillna(0)

        # 코인이 조건에 부합하는지 판단 
        z = 0
        if len(matching_coin_name_df) != 0 and trend_type == 'up_trend' and int(trend_reverse) == 0:
            for i in range(int(MASP), len(tied_time_df)):
                if float(masp[i]) == 0:
                    continue

                if float(masp[i]) > float(masp[i-1]):
                    z += 1
                else:
                    z = 0

                if z == int(trend_term):
                    Trend_list.append(coin)
                    Trend_value.append({'coin_name': coin, 'first_value': masp.iloc[i-(int(trend_term))], 'last_value': masp[i]})
        if len(matching_coin_name_df) != 0 and trend_type == 'down_trend' and int(trend_reverse) == 0:
            for i in range(int(MASP), len(tied_time_df)):
                if float(masp[i]) == 0:
                    continue

                if float(masp[i]) < float(masp[i-1]):
                    z += 1
                else:
                    z = 0

                if z == int(trend_term):
                    Trend_list.append(coin)
                    Trend_value.append({'coin_name': coin, 'first_value': masp.iloc[i-(int(trend_term))], 'last_value': masp[i]})


        if len(matching_coin_name_df) != 0 and trend_type == 'up_trend' and int(trend_reverse) == 1:
            for i in range(int(MASP), len(tied_time_df)):
                if float(masp[i]) == 0:
                    continue

                if z == int(trend_term):
                    if float(masp[i]) < float(masp[i-1]):
                        Trend_list.append(coin)
                        Trend_value.append({'coin_name': coin, 'first_value': masp.iloc[i-(int(trend_term) + 1)], 'last_value': masp[i]})

                if float(masp[i]) > float(masp[i-1]):
                    z += 1
                else:
                    z = 0

        if len(matching_coin_name_df) != 0 and trend_type == 'down_trend' and int(trend_reverse) == 1:
            for i in range(int(MASP), len(tied_time_df)):
                if z == int(trend_term):
                    if float(masp[i]) > float(masp[i-1]):
                        Trend_list.append(coin)
                        Trend_value.append({'coin_name': coin, 'first_value': masp.iloc[i-(int(trend_term) + 1)], 'last_value': masp[i]})

                if float(masp[i]) < float(masp[i-1]):
                    z += 1
                else:
                    z = 0
      except Exception as e:
        print(e)
    
    fn_end = datetime.datetime.now()
    print('trend spend time ::::::: ', fn_end - fn_start)
    print('trend end ::::::: ', len(Trend_list))
    print('-----------------------------------------------------------------------------------------------------------')
    return Trend_list, Trend_value
