import pandas as pd
import numpy as np

# 이평선 옵션, 현재시간, dataframe 전달 받아 조건에 맞는 코인 return
def MaspRecommend(nowstamp, coinList, dfList, chart_term, first_disparity, second_disparity, comparison):
        MaspL = []
        MaspValue = []
        print('masp:', len(coinList), '33333333333333333333333333333333333333333333333333333333333333333333333333')

        pd.set_option('display.max_columns', None)
        # 이격도 조건중 더 큰값 
        bigger = int(first_disparity)
        if bigger < int(second_disparity):
            bigger = int(second_disparity)

        # dataframe 생성 및 기준 시간 이후 데이터로 자르기
        times = int(chart_term[:-1])
        if chart_term[-1] == 'm':
            masTime = nowstamp - (bigger * (times) * 60)
        if chart_term[-1] == 'h':
            masTime = nowstamp - (bigger * (times) * 3600)

        df = pd.DataFrame(dfList)
        df['date'] = pd.to_datetime(df['time'])
        df2 = df.loc[df['S_time'] > masTime]

        # 코인별로 순회하며 조건에 맞는지 찾기
        for coin in coinList:
            #try:
                df3 = df2.loc[df['coin_name'] == coin].copy()

                # 시간 범위 내 거래량 0인 코인 빼기
                vol = df3['Volume'].sum()
                if vol == 0.0:
                    continue

                # 빈 시간 0 채움
                df3.loc[:, 'time'] = pd.to_datetime(df3['time'])
                df3.index = pd.to_datetime(df3['time'])
                df3 = df3[~df3.index.duplicated(keep='first')]
                df3.reset_index(drop=True, inplace=True)

                df3 = df3.set_index('time').resample('1H').asfreq()
                df3 = df3.fillna(method='ffill')

                # 생성한 dataframe을 chart term 단위 씩 묶어 dataframe 다시 생성 
                df4 = df3[(len(df3) % times):]
                df4.reset_index(drop=True, inplace=True)

                # 리스트를 times개씩 묶기
                new_df = df4.groupby(np.arange(len(df4)) // times).mean(numeric_only=True)

                dfFirst = new_df[-int(first_disparity):]
                dfSecond = new_df[-int(second_disparity):]

                # 첫번째, 두번째 이격도 옵션 이격도 찾기
                avgP1 = dfFirst['Close'].mean()
                avgP2 = dfSecond['Close'].mean()

                # 비교
                if comparison == '>=':
                    if len(df3) != 0 and avgP1 >= avgP2:
                        MaspL.append(coin)
                        MaspValue.append({'coin_name': coin, 'first_disparity': avgP1, 'second_disparity': avgP2})

                if comparison == '<=':
                    if len(df3) != 0 and avgP1 <= avgP2:
                        MaspL.append(coin)
                        MaspValue.append({'coin_name': coin, 'first_disparity': avgP1, 'second_disparity': avgP2})

            #except Exception as e:
                #print(e, coin, 'Masp error')

        print('masp', len(MaspL), '33333333333333333333333333333333333333333333333')

        return MaspL, MaspValue
