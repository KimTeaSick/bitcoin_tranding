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
        "date": value[7][0:19]
    }
    return R_VALUE


def TIME_Y4MMDDSSHHMMSS(value):
    return value.replace("-","").replace(" ","").replace(":","")[0:14]

def TODAY_TRADING_RESULT(value):
    buy = 0
    sell = 0
    if(value[0][0][0] != None): buy = value[0]
    if(value[1][0][0] != None): sell = value[1]
    R_VALUE={
        "total":round(value[2]),
        "deposit": round(value[3]),
        "buy":buy,
        "sell":sell,
    }
    return R_VALUE
