import requests
import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from recommends import priceFilter, transactionAmountFilter, MaspFilter, trendFilter, disparityFilter, MacdFilter

async def recommend_coin(options, minute_max, hour_max):
    with SessionLocal() as db:
        print('options ::::::: ', options)
        now = datetime.datetime.now()
        nowstamp = int(now.timestamp() / 60) * 60

        print('now ::: ::: ', datetime.datetime.utcfromtimestamp(nowstamp))

        minute_now_stamp = nowstamp - (minute_max * 60)
        df_minute_source = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= minute_now_stamp).all()
        df_minute_list = [
            {'idx': dfs.idx, 'coin_name': dfs.coin_name, 'S_time': dfs.S_time, 'time': dfs.time, 'Close': dfs.Close, 'Volume': dfs.Volume, 'Transaction_amount': dfs.Transaction_amount}
            for dfs in df_minute_source
        ]

        hour_now_stamp = nowstamp - (hour_max * 3600)
        df_hour_source = db.query(models.coin1HPrice).filter(models.coin1HPrice.STime >= hour_now_stamp).all()
        df_hour_list = [
            {'idx': dfs.idx, 'coin_name': dfs.coin_name, 'S_time': int(dfs.STime), 'time': dfs.time, 'Close': float(dfs.Close), 'Volume': float(dfs.Volume), 'Transaction_amount': float(dfs.Close) * float(dfs.Volume)}
            for dfs in df_hour_source
        ]

        coin_list = db.query(models.coinList).filter(models.coinList.warning == 0).all()
        coin_name_list = [coin.coin_name for coin in coin_list]
        current_coin = db.query(models.coinCurrentPrice).all()

        for current in current_coin:
            df_hour_list.append({
                'coin_name': current.coin_name,
                'S_time': int(current.S_time),
                'time': current.time,
                'Close': float(current.Close),
                'Volume': float(0.0),
                'Transaction_amount': float(current.Close) * float(0.0)
            })

        result_dict = {
            'Price': [],
            'TransactionAmount': [],
            'Disparity': [],
            'Masp': [],
            'Trend': [],
            'MACD': []
        }

        for option in options:
            term = option.get('chart_term', '')
            if option['option'] == 'Price':
                filtered_coins, values = priceFilter.priceRecommend(nowstamp, coin_name_list, df_minute_list, option['low_price'], option['high_price'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['Price'].extend(values)

            elif option['option'] == 'TransactionAmount':
                if term.endswith('m'):
                    filtered_coins, values = transactionAmountFilter.transactioAmountRecommend(nowstamp, coin_name_list, df_minute_list, term, option['low_transaction_amount'], option['high_transaction_amount'])
                elif term.endswith('h'):
                    filtered_coins, values = transactionAmountFilter.transactioAmountRecommend(nowstamp, coin_name_list, df_hour_list, term, option['low_transaction_amount'], option['high_transaction_amount'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['TransactionAmount'].extend(values)

            elif option['option'] == 'MASP':
                if term.endswith('m'):
                    filtered_coins, values = MaspFilter.MaspRecommend(nowstamp, coin_name_list, df_minute_list, term, option['first_disparity'], option['second_disparity'], option['comparison'])
                elif term.endswith('h'):
                    filtered_coins, values = MaspFilter.MaspRecommend(nowstamp, coin_name_list, df_hour_list, term, option['first_disparity'], option['second_disparity'], option['comparison'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['Masp'].extend(values)

            elif option['option'] == 'Disparity':
                if term.endswith('m'):
                    filtered_coins, values = disparityFilter.disparityRecommend(nowstamp, coin_name_list, df_minute_list, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                elif term.endswith('h'):
                    filtered_coins, values = disparityFilter.disparityRecommend(nowstamp, coin_name_list, df_hour_list, term, option['disparity_term'], option['low_disparity'], option['high_disparity'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['Disparity'].extend(values)

            elif option['option'] == 'Trend':
                if term.endswith('m'):
                    filtered_coins, values = trendFilter.trendRecommend(nowstamp, coin_name_list, df_minute_list, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                elif term.endswith('h'):
                    filtered_coins, values = trendFilter.trendRecommend(nowstamp, coin_name_list, df_hour_list, term, option['MASP'], option['trend_term'], option['trend_type'], option['trend_reverse'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['Trend'].extend(values)

            elif option['option'] == 'MACD':
                if term.endswith('m'):
                    filtered_coins, values = MacdFilter.MacdRecommend(nowstamp, coin_name_list, df_minute_list, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                elif term.endswith('h'):
                    filtered_coins, values = MacdFilter.MacdRecommend(nowstamp, coin_name_list, df_hour_list, term, option['short_disparity'], option['long_disparity'], option['signal'], option['up_down'])
                coin_name_list = set(coin_name_list) & set(filtered_coins)
                result_dict['MACD'].extend(values)

        response = requests.get("https://api.bithumb.com/public/ticker/ALL_KRW", headers={"accept": "application/json"})
        data = response.json()["data"]

        recommend_dict = []
        for coin in coin_list:
            if coin.coin_name in coin_name_list:
                name = coin.coin_name[:-4]
                recommend_dict.append({name: data[name]})

        now2 = datetime.datetime.now()
        print('spend time ::::::: ', now2 - now1)
        return {'recommends': recommend_dict, **result_dict}

if __name__ == '__main__':
    options = [
        # Define your options here
    ]
    minute_max = 60
    hour_max = 24
    recommendations = asyncio.run(recommend_coin(options, minute_max, hour_max))
    print(recommendations)
