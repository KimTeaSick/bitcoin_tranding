from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base


class autoTradingStatus(Base):
    __tablename__ = 'nc_b_now_auto_status_t'

    idx = Column(Integer, primary_key=True)

    status = Column(Integer)
    start_date = Column(String(100))


class tradingOption(Base):
    __tablename__ = "nc_b_trading_option_t"
    idx = Column(Integer, primary_key=True)
    name = Column(String(100))
    insert_time = Column(String(100))
    update_time = Column(String(100))
    used = Column(Integer)


class tradingAccountOption(Base):
    __tablename__ = "nc_c_account_option_t"
    idx = Column(Integer, primary_key=True)
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


class orderCoin(Base):
    __tablename__ = 'nc_r_order_coin_t'

    coin = Column(String(100), primary_key=True)

    status = Column(Integer)
    transaction_time = Column(String(100))
    conclusion_time = Column(String(100))
    order_id = Column(String(100))
    cancel_time = Column(String(100))
    sell_reason = Column(String(100))


class possessionCoin(Base):
    __tablename__ = 'nc_r_possession_coin_t'
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


class tradingSellOption(Base):
    __tablename__ = "nc_c_sell_option_t"
    idx = Column(Integer, primary_key=True)
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
