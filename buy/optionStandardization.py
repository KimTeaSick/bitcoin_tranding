def OptionStandardization(priceOption, transactionAmountOption, maspOption, trendOption, disparityOption, macdOption):
    options = []
    mMax = 0
    hMax = 0

    if priceOption.flag == 1 and priceOption.high_price != 0:
        mMax = max(mMax, 5)
        options.append({
            'option': 'Price',
            'low_price': priceOption.low_price,
            'high_price': priceOption.high_price
        })

    if transactionAmountOption.flag == 1 and transactionAmountOption.high_transaction_amount != 0:
        term_value = int(transactionAmountOption.chart_term[:-1])
        if transactionAmountOption.chart_term[-1] == 'm':
            mMax = max(mMax, term_value)
        elif transactionAmountOption.chart_term[-1] == 'h':
            hMax = max(hMax, term_value)
        options.append({
            'option': 'TransactionAmount',
            'chart_term': transactionAmountOption.chart_term,
            'low_transaction_amount': transactionAmountOption.low_transaction_amount,
            'high_transaction_amount': transactionAmountOption.high_transaction_amount
        })

    if maspOption.flag == 1 and maspOption.first_disparity != 0 and maspOption.second_disparity != 0:
        term_value = int(maspOption.chart_term[:-1])
        first_disparity_max = maspOption.first_disparity * term_value
        second_disparity_max = maspOption.second_disparity * term_value
        if maspOption.chart_term[-1] == 'm':
            mMax = max(mMax, first_disparity_max, second_disparity_max)
        elif maspOption.chart_term[-1] == 'h':
            hMax = max(hMax, first_disparity_max, second_disparity_max)
        options.append({
            'option': 'MASP',
            'chart_term': maspOption.chart_term,
            'first_disparity': maspOption.first_disparity,
            'second_disparity': maspOption.second_disparity,
            'comparison': maspOption.comparison
        })

    if disparityOption.flag == 1 and disparityOption.chart_term != 0:
        term_value = int(disparityOption.chart_term[:-1])
        disparity_max = disparityOption.disparity_term * term_value
        if disparityOption.chart_term[-1] == 'm':
            mMax = max(mMax, disparity_max)
        elif disparityOption.chart_term[-1] == 'h':
            hMax = max(hMax, disparity_max)
        options.append({
            'option': 'Disparity',
            'chart_term': disparityOption.chart_term,
            'disparity_term': disparityOption.disparity_term,
            'low_disparity': disparityOption.low_disparity,
            'high_disparity': disparityOption.high_disparity
        })

    if trendOption.flag == 1 and trendOption.trend_term != 0 and trendOption.MASP != 0:
        term_value = int(trendOption.chart_term[:-1])
        trend_max = (trendOption.trend_term + 2 + trendOption.MASP) * term_value
        if trendOption.chart_term[-1] == 'm':
            mMax = max(mMax, trend_max)
        elif trendOption.chart_term[-1] == 'h':
            hMax = max(hMax, trend_max)
        options.append({
            'option': 'Trend',
            'chart_term': trendOption.chart_term,
            'trend_term': trendOption.trend_term,
            'trend_type': trendOption.trend_type,
            'trend_reverse': trendOption.trend_reverse,
            'MASP': trendOption.MASP
        })

    if macdOption.flag == 1 and macdOption.short_disparity != 0 and macdOption.long_disparity != 0:
        term_value = int(macdOption.chart_term[:-1])
        macd_max = (macdOption.long_disparity * 2 + macdOption.signal) * term_value
        if macdOption.chart_term[-1] == 'm':
            mMax = max(mMax, macd_max)
        elif macdOption.chart_term[-1] == 'h':
            hMax = max(hMax, macd_max)
        options.append({
            'option': 'MACD',
            'chart_term': macdOption.chart_term,
            'short_disparity': macdOption.short_disparity,
            'long_disparity': macdOption.long_disparity,
            'signal': macdOption.signal,
            'up_down': macdOption.up_down
        })

    return options, mMax, hMax
