from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base


class coinList(Base):
    __tablename__ = "nc_r_coin_list_t"
    idx = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String(100))
    warning = Column(String(100))
    delflag = Column(Integer)


class coinCurrentCandlePrice(Base):
    __tablename__ = "nc_p_coin_current_candle_price_t"
    coin_name = Column(String(100), primary_key=True)
    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class searchOption(Base):
    __tablename__ = "nc_b_search_option_t"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    Create_date = Column(String(100))
    Update_date = Column(String(100))
    used = Column(Integer)


class PriceOption(Base):
    __tablename__ = "nc_c_pr_price_t"
    idx = Column(Integer, primary_key=True, index=True)
    low_price = Column(Integer)
    high_price = Column(Integer)
    flag = Column(Integer)


class TransactionAmountOption(Base):
    __tablename__ = "nc_c_pr_transaction_amount_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    low_transaction_amount = Column(Integer)
    high_transaction_amount = Column(Integer)
    flag = Column(Integer)


class MASPOption(Base):
    __tablename__ = "nc_c_masp_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    first_disparity = Column(Integer)
    second_disparity = Column(Integer)
    comparison = Column(String(100))
    flag = Column(Integer)

class DisparityOption(Base):
    __tablename__ = "nc_c_disparity_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    disparity_term = Column(String(100))
    low_disparity = Column(Integer)
    high_disparity = Column(Integer)
    flag = Column(Integer)


class TrendOption(Base):
    __tablename__ = "nc_c_trend_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    MASP = Column(Integer)
    trend_term = Column(Integer)
    trend_reverse = Column(Integer)
    trend_type = Column(String(100))
    flag = Column(Integer)


class MACDOption(Base):
    __tablename__ = "nc_c_macd_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    short_disparity = Column(Integer)
    long_disparity = Column(Integer)
    up_down = Column(String(100))
    signal = Column(Integer)
    flag = Column(Integer)

# candle performance ============================================================================================================


class coinMinPrice(Base):
    __tablename__ = "nc_p_min_bithumb_t"

    idx = Column(Integer, primary_key=True, index=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin3MPrice(Base):
    __tablename__ = "nc_p_3min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin5MPrice(Base):
    __tablename__ = "nc_p_5min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin10MPrice(Base):
    __tablename__ = "nc_p_10min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin30MPrice(Base):
    __tablename__ = "nc_p_30min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin1HPrice(Base):
    __tablename__ = "nc_p_1H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    # empty_count = Column(Integer, default=0)


class coin6HPrice(Base):
    __tablename__ = "nc_p_6H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin12HPrice(Base):
    __tablename__ = "nc_p_12H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)


class coin1DPrice(Base):
    __tablename__ = "nc_p_1D_bithumb_t"

    idx = Column(Integer, primary_key=True)

    STime = Column(Integer)
    Open = Column(String(100))
    Close = Column(String(100))
    High = Column(String(100))
    Low = Column(String(100))
    Volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

# ==========================================================================================================================================조건 부합 코인 저장


class recommendList(Base):
    __tablename__ = "nc_f_recommend_coin_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    catch_price = Column(String(100))
    option_name = Column(String(100))

# class recommendList(Base):
#     __tablename__ = "nc_f_recommend_coin_list_t"

#     idx = Column(Integer, primary_key=True)

#     coin_name = Column(String(100))
#     catch_price = Column(String(100))
#     option_name = Column(String(100))

# nmsVersion performance ================================================================================================


class coinCurrentPrice(Base):
    __tablename__ = "nc_p_coin_current_price_t"

    coin_name = Column(String(100), primary_key=True)

    S_time = Column(Integer)
    time = Column(String(100))
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Volume = Column(Float)
    Transaction_amount = Column(Float)


class coinPrice1M(Base):
    __tablename__ = "nc_p_1m_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    S_time = Column(Integer)
    time = Column(String(100))
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Ask_price = Column(Float)
    Avg_price = Column(Float)
    Volume = Column(Float)
    Transaction_amount = Column(Float)
    Disparity = Column(Float)


class coinPrice30M(Base):
    __tablename__ = "nc_p_30m_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    S_time = Column(Integer)
    time = Column(String(100))
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Ask_price = Column(Float)
    Avg_price = Column(Float)
    Volume = Column(Float)
    Transaction_amount = Column(Float)
    Disparity = Column(Float)


class coinPrice1H(Base):
    __tablename__ = "nc_p_1h_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    S_time = Column(Integer)
    time = Column(String(100))
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Ask_price = Column(Float)
    Avg_price = Column(Float)
    Volume = Column(Float)
    Transaction_amount = Column(Float)
    Disparity = Column(Float)


class tradingOption(Base):
    __tablename__ = "nc_b_trading_option_t"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    insert_time = Column(String(100))
    update_time = Column(String(100))
    used = Column(Integer)


class tradingAccountOtion(Base):
    __tablename__ = "nc_c_account_option_t"

    idx = Column(Integer, primary_key=True)

    name = Column(String(100))
    price_count = Column(Integer)
    loss_cut_under_percent = Column(Integer)
    loss = Column(Integer)
    loss_cut_under_call_price_sell_all = Column(Integer)
    loss_cut_under_coin_specific_percent = Column(Integer)
    loss_cut_under_call_price_specific_coin = Column(Integer)
    loss_cut_over_percent = Column(Integer)
    gain = Column(Integer)
    loss_cut_over_call_price_sell_all = Column(Integer)
    loss_cut_over_coin_specific_percent = Column(Integer)
    loss_cut_over_call_price_specific_coin = Column(Integer)
    buy_cancle_time = Column(Integer)
    sell_cancle_time = Column(Integer)
    loss = Column(Integer)
    gain = Column(Integer)


class tradingBuyOption(Base):
    __tablename__ = "nc_c_buy_option_t"

    idx = Column(Integer, primary_key=True)

    name = Column(String(100))

    percent_to_buy_method = Column(Integer)
    price_to_buy_method = Column(Integer)
    callmoney_to_buy_method = Column(Integer)
    checkbox = Column(Integer)


class tradingSellOption(Base):
    __tablename__ = "nc_c_sell_option_t"

    idx = Column(Integer, primary_key=True)

    name = Column(String(100))

    upper_percent_to_price_condition = Column(Integer)
    down_percent_to_price_condition = Column(Integer)
    disparity_for_upper_case = Column(Integer)
    upper_percent_to_disparity_condition = Column(Integer)
    disparity_for_down_case = Column(Integer)
    down_percent_to_disparity_condition = Column(Integer)
    call_money_to_sell_method = Column(String(100))
    percent_to_split_sell = Column(Integer)
    shot_MACD_value = Column(Integer)
    long_MACD_value = Column(Integer)
    MACD_signal_value = Column(Integer)
    trailing_start_percent = Column(String(100))
    trailing_stop_percent = Column(String(100))
    trailing_order_call_price = Column(String(100))


class possessionCoin(Base):
    __tablename__ = 'nc_r_possession_coin_t'
    # idx = Column(Integer, primary_key=True)
    coin = Column(String(100), primary_key=True)

    unit = Column(String(100))
    price = Column(String(100))
    total = Column(String(100))
    fee = Column(String(100))
    status = Column(Integer)
    transaction_time = Column(String(100))
    conclusion_time = Column(String(100))
    order_id = Column(String(100))
    cancel_time = Column(String(100))
    macd_chart = Column(String(100))
    disparity_chart = Column(String(100))
    optionName = Column(String(100))
    trailingstop_flag = Column(Integer)
    max = Column(String(100))


class possessionLog(Base):
    __tablename__ = 'nc_p_possession_coin_his_t'

    idx = Column(Integer, primary_key=True)

    coin = Column(String(100))
    unit = Column(String(100))
    price = Column(String(100))
    total = Column(String(100))
    fee = Column(String(100))
    status = Column(Integer)
    transaction_time = Column(String(100))
    conclusion_time = Column(String(100))
    type = Column(String(100))
    order_id = Column(String(100))
    sell_reason = Column(String(100))


class orderCoin(Base):
    __tablename__ = 'nc_r_order_coin_t'

    coin = Column(String(100), primary_key=True)

    status = Column(Integer)
    transaction_time = Column(String(100))
    conclusion_time = Column(String(100))
    order_id = Column(String(100))
    cancel_time = Column(String(100))
    sell_reason = Column(String(100))


class autoTradingStatus(Base):
    __tablename__ = 'nc_b_now_auto_status_t'

    idx = Column(Integer, primary_key=True)

    status = Column(Integer)
    start_date = Column(String(100))
