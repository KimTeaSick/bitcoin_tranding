# 호가 계산 함수 
def askingPrice(price):
    result:float = 0.0
    if price < 1:
        result = 0.0001
    elif price >= 1 and price < 10:
        result = 0.001
    elif price >= 10 and price < 100:
        result = 0.01
    elif price >= 100 and price < 1000:
        result = 0.1
    elif price >= 1000 and price < 5000:
        result = 1
    elif price >= 5000 and price < 10000:
        result = 5
    elif price >= 10000 and price < 50000:
        result = 10
    elif price >= 50000 and price < 100000:
        result = 50
    elif price >= 100000 and price < 500000:
        result = 100
    elif price >= 500000 and price < 1000000:
        result = 500
    elif price >= 1000000:
        result = 1000

    return result
