def ORDER_LIST_CHANGER(value):
    R_VALUE = {
        "coin_name" : value[0],
        "unit" : value[1],
        "price" : value[2],
        "total_price" : value[3],
        "fee" : value[4],
        "type" : value[5],
        "date" : str(value[6]),
    }
    return R_VALUE

def TRADING_LIST(value):
    R_VALUE = { 
        "coin_name": value[1], 
        "unit":value[2], 
        "price": value[3], 
        "total": value[4], 
        "fee": value[5],
        "status": value[6],
        "date": value[7][0:19],
        "sell_reason": value[11]
    }
    return R_VALUE

def TIME_Y4MMDDSSHHMMSS(value):
    return value.replace("-","").replace(" ","").replace(":","")[0:14]

def TODAY_TRADING_RESULT(value):
    print("TODAY_TRADING_RESULT :::: ", value)
    buy = 0
    sell = 0
    if(value[0][0][0] != None): 
        print("value[0][0] :::: ", value[0][0])
        buy = value[0]
    if(value[1][0][0] != None): 
        print("value[1][0] :::: ", value[1][0])
        sell = value[1]
    R_VALUE={
        "total":round(value[2]),
        "deposit": round(value[3]),
        "buy":buy,
        "sell":sell,
    }
    return R_VALUE

def SEARCH_CONDITION(value):
    R_VALUE = {
        "name": value[0][0],
        "low_price": value[0][1],
        "high_price": value[0][2],
        "TA_chart_term": value[0][3],
        "low_transaction_amount": value[0][4],
        "high_transaction_amount": value[0][5],
        "MASP_chart_term": value[0][6],
        "first_disparity": value[0][7],
        "comparison": value[0][8],
        "second_disparity": value[0][9],
        "trend_chart_term": value[0][10],
        "MASP": value[0][11],
        "trend_term": value[0][12],
        "trend_type": value[0][13],
        "trend_reverse": value[0][14],
        "disparity_chart_term": value[0][15],
        "disparity_term": value[0][16],
        "low_disparity": value[0][17],
        "high_disparity": value[0][18],
        "MACD_chart_term": value[0][19],
        "short_disparity": value[0][20],
        "long_disparity": value[0][21],
        "signal": value[0][22],
        "up_down": value[0][23]
    }
    return R_VALUE

def TRADING_CONDITION(value):
    R_VALUE = {
        "name": value[0][0],
        "price_count": value[0][1],
        "loss_cut_under_percent": value[0][2],
        "loss_cut_under_call_price_sell_all": value[0][3],
        "loss_cut_under_coin_specific_percent": value[0][4],
        "loss_cut_under_call_price_specific_coin": value[0][5],
        "loss_cut_over_percent": value[0][6],
        "loss_cut_over_call_price_sell_all": value[0][7],
        "loss_cut_over_coin_specific_percent": value[0][8],
        "loss_cut_over_call_price_specific_coin": value[0][9],
        "buy_cancle_time": value[0][10],
        "sell_cancle_time": value[0][11],
        "percent_to_buy_method": value[0][12],
        "price_to_buy_method": value[0][13],
        "callmoney_to_buy_method": value[0][14],
        "upper_percent_to_price_condition": value[0][15],
        "down_percent_to_price_condition": value[0][16],
        "disparity_for_upper_case": value[0][17],
        "upper_percent_to_disparity_condition": value[0][18],
        "disparity_for_down_case": value[0][19],
        "down_percent_to_disparity_condition": value[0][20],
        "call_money_to_sell_method": value[0][21],
        "percent_to_split_sell": value[0][22],
        "short_MACD_value": value[0][23],
        "long_MACD_value": value[0][24],
        "MACD_signal_value": value[0][25],
    }
    return R_VALUE

def BITHUMB_COIN_LIST(value):
    R_VALUE = []
    for coin in value:
        R_VALUE.append({"en_name":str(coin[0]).replace("_KRW",""), "kr_name":coin[1], "warning": coin[2]})
    return R_VALUE

def POSSESSION_COIN_LIST(coin, coin_now_price):
    print("POSSESSION_COIN_LIST coin :::: ", coin)

    def type_one(coin, coin_now_price, status):
        return {"coin" : coin[0], 
            "status" : status, 
            "info" : { 
                    "unit" : coin[1],
                    "now_price" : coin_now_price,
                    "buy_price" : coin[2],
                    "buy_total_price" : coin[3],
                    "evaluate_price" : float(coin_now_price) * float(coin[1]), #평가금액
                    "profit" : float(coin_now_price) * float(coin[1]) - float(coin[3]),
                    "rate" : ((float(coin_now_price) * float(coin[1]) - float(coin[3])) / float(coin[3])) * 100
                    }
            }
    def type_two(coin, coin_now_price, status):
        return {"coin" : coin[0], 
            "status" : status, 
            "info" : { 
                    "unit" : coin[1],
                    "now_price" : coin_now_price,
                    "buy_price" : coin[2],
                    "buy_total_price" : coin[3],
                    "evaluate_price" : 0,
                    "profit" : 0,
                    "rate" : 0
                    }
            }
    
    if coin[5] == 0:
        return type_one(coin, coin_now_price, "보유중")
    elif coin[5] == 1:
        return type_two(coin, coin_now_price, "매수 중")
    elif coin[5] == 2:
        return type_two(coin, coin_now_price, "분할 매수")
    elif coin[5] == 3:
        return type_one(coin, coin_now_price, "첫번째 매도 중")
    elif coin[5] == 4:
        return type_one(coin, coin_now_price, "메도 취소")
    elif coin[5] == 5:
        return type_one(coin, coin_now_price, "매도 중")
    elif coin[5] == 6:
        return type_two(coin, coin_now_price, "매도 완료")