from datetime import datetime
import pandas as pd

def MaspRecommend(nowstamp, coinList, dfList, chart_term, first_disparity, second_disparity, comparison):
        MaspL = []

        bigger = int(first_disparity)
        if bigger < int(second_disparity):
            bigger = int(second_disparity)
        times = int(chart_term[:-1])

        if chart_term[-1] == 'm':
            time = nowstamp - (bigger * (times) * 60)
        if chart_term[-1] == 'h':
            time = nowstamp - (bigger * (times) * 3600)

        df = pd.DataFrame(dfList)
        print(df)
        df2 = df.loc[df['S_time'] > time]


        for coin in coinList:
            try:
                df2 = df.loc[df['coin_name'] == coin]
                df3 = df2[- int(first_disparity):]
                df4 = df2[- int(second_disparity):]

                vol = df3['Volume'].sum()
                if vol == 0.0:
                    continue

                avgP1 = df3['Close'].mean()
                Recent1 = df3['Close'].iloc[-1]
                disP1 = (avgP1 / Recent1) * 100

                avgP2 = df4['Close'].mean()
                Recent2 = df4['Close'].iloc[-1]
                disP2 = (avgP2 / Recent2) * 100

                if comparison == '>=':
                    if disP1 >= disP2:
                        MaspL.append(coin)
                if comparison == '<=':
                    if disP1 <= disP2:
                        MaspL.append(coin)
            except Exception as e:
                print(e, coin, 'Masp error')

        return MaspL
