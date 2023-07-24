import pandas as pd
import numpy as np
import datetime

# 이평선 옵션, 현재시간, dataframe 전달 받아 조건에 맞는 코인 return
def MaspRecommend(nowstamp, coinList, dfList, chart_term, first_disparity, second_disparity, comparison):
        print('-----------------------------------------------------------------------------------------------------------')
        print('masp start ::::::: ')
        print('masp parameter ::::::: ', nowstamp, len(coinList), len(dfList), chart_term, first_disparity, second_disparity, comparison)
        print('before condition pass coins ::::::: ', len(coinList))
        fn_start = datetime.datetime.now()
        Masp_list = []
        Masp_value = []

        pd.set_option('display.max_columns', None)

        # 이격도 조건중 더 큰값 
        bigger = int(first_disparity) if int(first_disparity) < int(second_disparity) else int(second_disparity)
        # dataframe 생성 및 기준 시간 이후 데이터로 자르기
        times = int(chart_term[:-1])
        masTime = nowstamp - (bigger * (times) * 60) if chart_term[-1] == 'm' else nowstamp - (bigger * (times) * 3600)

        df = pd.DataFrame(dfList)
        df['date'] = pd.to_datetime(df['time'])
        time_satisfied_df = df.loc[df['S_time'] > masTime]

        # 코인별로 순회하며 조건에 맞는지 찾기
        for coin in coinList:
            #try:
                matching_coin_name_df = time_satisfied_df.loc[df['coin_name'] == coin].copy()

                # 시간 범위 내 거래량 0인 코인 빼기
                vol = matching_coin_name_df['Volume'].sum()
                if vol == 0.0:
                    continue

                # 빈 시간 0 채움
                matching_coin_name_df.loc[:, 'time'] = pd.to_datetime(matching_coin_name_df['time'])
                matching_coin_name_df.index = pd.to_datetime(matching_coin_name_df['time'])
                matching_coin_name_df = matching_coin_name_df[~matching_coin_name_df.index.duplicated(keep='first')]
                matching_coin_name_df.reset_index(drop=True, inplace=True)

                matching_coin_name_df = matching_coin_name_df.set_index('time').resample('1H').asfreq()
                matching_coin_name_df = matching_coin_name_df.fillna(method='ffill')

                # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
                tied_chart_term_df = matching_coin_name_df[(len(matching_coin_name_df) % times):]
                tied_chart_term_df.reset_index(drop=True, inplace=True)

                # 리스트를 times개씩 묶기
                tied_time_df = tied_chart_term_df.groupby(np.arange(len(tied_chart_term_df)) // times).mean(numeric_only=True)

                dfFirst = tied_time_df[-int(first_disparity):]
                dfSecond = tied_time_df[-int(second_disparity):]

                # 첫번째, 두번째 이격도 옵션 이격도 찾기
                avgP1 = dfFirst['Close'].mean()
                avgP2 = dfSecond['Close'].mean()

                # 비교
                if comparison == '>=':
                    if len(matching_coin_name_df) != 0 and avgP1 >= avgP2:
                        Masp_list.append(coin)
                        Masp_value.append({'coin_name': coin, 'first_disparity': avgP1, 'second_disparity': avgP2})

                if comparison == '<=':
                    if len(matching_coin_name_df) != 0 and avgP1 <= avgP2:
                        Masp_list.append(coin)
                        Masp_value.append({'coin_name': coin, 'first_disparity': avgP1, 'second_disparity': avgP2})

            #except Exception as e:
                #print(e, coin, 'Masp error')
        fn_end = datetime.datetime.now()
        print('masp spend time ::::::: ', fn_end - fn_start)
        print('masp end ::::::: ', len(Masp_list))
        print('-----------------------------------------------------------------------------------------------------------')

        return Masp_list, Masp_value
