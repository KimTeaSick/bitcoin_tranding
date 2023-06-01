from datetime import datetime
import pandas as pd

# 이평선 옵션, 현재시간, dataframe 전달 받아 조건에 맞는 코인 return
def MaspRecommend(nowstamp, coinList, dfList, chart_term, first_disparity, second_disparity, comparison):
        MaspL = []

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
        df2 = df.loc[df['S_time'] > masTime]

        # 코인별로 순회하며 조건에 맞는지 찾기
        for coin in coinList:
            try:
                df3 = df2.loc[df['coin_name'] == coin]
                df4 = df3[- int(first_disparity):]
                df5 = df3[- int(second_disparity):]

                # 시간 범위 내 거래량 0인 코인 빼기
                vol = df3['Volume'].sum()
                if vol == 0.0:
                    continue

                # 첫번째, 두번째 이격도 옵션 이격도 찾기
                avgP1 = df4['Close'].mean()
                Recent1 = df4['Close'].iloc[-1]
                disP1 = (avgP1 / Recent1) * 100

                avgP2 = df5['Close'].mean()
                Recent2 = df5['Close'].iloc[-1]
                disP2 = (avgP2 / Recent2) * 100

                # 비교
                if comparison == '>=':
                    if disP1 >= disP2:
                        MaspL.append(coin)

                if comparison == '<=':
                    if disP1 <= disP2:
                        MaspL.append(coin)

            except Exception as e:
                print(e, coin, 'Masp error')

        return MaspL
