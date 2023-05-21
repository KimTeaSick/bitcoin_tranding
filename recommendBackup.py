import requests
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
import pandas as pd
from sqlalchemy import create_engine, desc

# 조건 식에 따른 코인 필터 함수
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

def recommendCoin(options):
    now1 = datetime.datetime.now()
    # 최근 10분 거래량 없는 코인 필터
    current = db.query(models.coinCurrentPrice).filter(models.coinCurrentPrice.empty_count < 10).all()

    recommendList = []
    for coin in current:
        recommendList.append(coin.coin_name)

    # 옵션중 현재가, 거래량, 거래대금 있을때 코인 조건 탐색
    for option in options:
        recommendList2 = []
        if option['option'] == 'P_range':
            for coin in current:
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']):
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'V_volume':
            for coin in current:
                if float(coin.Volume) > float(option['first_value']) and float(coin.Volume) < float(option['second_value']):
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'P_transactionAmount':
            for coin in current:
                if float(coin.Volume) * float(coin.Close) > float(option['first_value']) and float(coin.Volume) < float(option['second_value']):
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

    # =======================================================================================================================================================================0514 옵션명 바꿈
    # 과거 데이터 필요 옵션 별 코인 조건 탐색
    for option in options:
        recommendList2 = []
        if option['option'] == 'P_fluctuation':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'V_avg_volume':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MASP_comparison':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MASP_comparison_double':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MASP_disparity':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MASP_trend':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'D_overRV':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'D_rangeRV':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'D_RV_up_down':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'D_trend':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'D_reverse':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_line_over':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_line_comparison':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_value_over':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_value_up_down':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_value_range':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_trend':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACD_reverse':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACDS_value_over':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACDS_value_up_down':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACDS_value_range':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACDS_trend':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

        if option['option'] == 'MACDS_reverse':
            for coin in recommendList:
                # 계산 필요
                if float(coin.Close) > float(option['first_value']) and float(coin.Close) < float(option['second_value']): # 조건식 수정 필요
                    recommendList2.append(coin.coin_name)
            recommendList = list(filter(lambda x: x in recommendList2, recommendList))

    for option in options:
        print(len(recommendList), option['option'])

    now2 = datetime.datetime.now()

    print(now2 - now1)
    return options