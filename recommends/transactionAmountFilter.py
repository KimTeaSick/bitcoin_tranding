# 거래대금 데이터, 범위 받아 조건에 맞는 코인 리턴 (수집기 수정후 수집기데이터 사용으로 수정예정)
def transactioAmountRecommend(coinList, lowTransactionAmount, highTransactionAmount):
    transactionAmountL = []

    for coin in coinList:
        if coin['Close'] > float(lowTransactionAmount) and coin['Close'] < float(highTransactionAmount):
            transactionAmountL.append(coin['name'])

    return transactionAmountL
