def transactioAmountRecommend(coinList, lowTransactionAmount, highTransactionAmount):
    transactionAmountL = []

    for coin in coinList:
        if coin['Close'] > float(lowTransactionAmount) and coin['Close'] < float(highTransactionAmount):
            transactionAmountL.append(coin['name'])

    return transactionAmountL
