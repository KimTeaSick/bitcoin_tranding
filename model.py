from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint, Text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class cp_r_coin_list_t(Base):
    __tablename__ = "cp_r_coin_list_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    coin_name = Column(String(255))
    warning = Column(String(255))
    delflag = Column(Integer)


class cp_p_coin_current_candle_price_t(Base):
    __tablename__ = "cp_p_coin_current_candle_price_t"

    coin_name = Column(String(255), primary_key=True)
    stime = Column(Integer)
    open_price = Column(String(255))
    close_price = Column(String(255))
    high_price = Column(String(255))
    low_price = Column(String(255))
    volume = Column(String(255))
    time_stamp = Column(String(255))
    empty_count = Column(Integer, default=0)


class cp_b_search_option_t(Base):
    __tablename__ = "cp_b_search_option_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    create_date = Column(String(255))
    update_date = Column(String(255))


class cp_c_pr_price_t(Base):
    __tablename__ = "cp_c_pr_price_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    low_price = Column(Integer)
    high_price = Column(Integer)
    flag = Column(Integer)


class cp_c_pr_transaction_amount_t(Base):
    __tablename__ = "cp_c_pr_transaction_amount_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    chart_term = Column(String(255))
    low_transaction_amount = Column(Integer)
    high_transaction_amount = Column(Integer)
    flag = Column(Integer)


class cp_c_masp_t(Base):
    __tablename__ = "cp_c_masp_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    chart_term = Column(String(255))
    first_disparity = Column(Integer)
    second_disparity = Column(Integer)
    comparison = Column(String(255))
    flag = Column(Integer)


class cp_c_disparity_t(Base):
    __tablename__ = "cp_c_disparity_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    chart_term = Column(String(255))
    disparity_term = Column(String(255))
    low_disparity = Column(Integer)
    high_disparity = Column(Integer)
    flag = Column(Integer)


class cp_c_trend_t(Base):
    __tablename__ = "cp_c_trend_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    chart_term = Column(String(255))
    masp = Column(Integer)
    trend_term = Column(Integer)
    trend_reverse = Column(Integer)
    trend_type = Column(String(255))
    flag = Column(Integer)


class cp_c_macd_t(Base):
    __tablename__ = "cp_c_macd_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    chart_term = Column(String(255))
    short_disparity = Column(Integer)
    long_disparity = Column(Integer)
    up_down = Column(String(255))
    signal = Column(Integer)
    flag = Column(Integer)


class cp_p_min_bithumb_t(Base):
    __tablename__ = "cp_p_min_bithumb_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    stime = Column(Integer)
    open_price = Column(String(255))
    close_price = Column(String(255))
    high_price = Column(String(255))
    low_price = Column(String(255))
    volume = Column(String(255))
    coin_name = Column(String(255))
    time_stamp = Column(String(255))
    empty_count = Column(Integer, default=0)


class cp_f_recommend_coin_t(Base):
    __tablename__ = "cp_f_recommend_coin_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    coin_name = Column(String(255))
    catch_price = Column(String(255))
    option_name = Column(String(255))


class cp_p_coin_current_price_t(Base):
    __tablename__ = "cp_p_coin_current_price_t"

    coin_name = Column(String(255), primary_key=True)
    s_time = Column(Integer)
    time_stamp = Column(String(255))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)
    transaction_amount = Column(Float)


class cp_b_trading_option_t(Base):
    __tablename__ = "cp_b_trading_option_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    insert_time = Column(String(255))
    update_time = Column(String(255))


class cp_c_account_option_t(Base):
    __tablename__ = "cp_c_account_option_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
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


class cp_c_buy_option_t(Base):
    __tablename__ = "cp_c_buy_option_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    percent_to_buy_method = Column(Integer)
    price_to_buy_method = Column(Integer)
    callmoney_to_buy_method = Column(Integer)
    checkbox = Column(Integer)


class cp_c_sell_option_t(Base):
    __tablename__ = "cp_c_sell_option_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    upper_percent_to_price_condition = Column(Integer)
    down_percent_to_price_condition = Column(Integer)
    disparity_for_upper_case = Column(Integer)
    upper_percent_to_disparity_condition = Column(Integer)
    disparity_for_down_case = Column(Integer)
    down_percent_to_disparity_condition = Column(Integer)
    call_money_to_sell_method = Column(String(255))
    percent_to_split_sell = Column(Integer)
    shot_macd_value = Column(Integer)
    long_macd_value = Column(Integer)
    macd_signal_value = Column(Integer)
    trailing_start_percent = Column(String(255))
    trailing_stop_percent = Column(String(255))
    trailing_order_call_price = Column(String(255))


class cp_r_possession_coin_t(Base):
    __tablename__ = "cp_r_possession_coin_t"

    coin = Column(String(255), primary_key=True)
    user_idx = Column(Integer, primary_key=True)
    unit = Column(String(255))
    price = Column(String(255))
    total = Column(String(255))
    fee = Column(String(255))
    status = Column(Integer)
    transaction_time = Column(String(255))
    conclusion_time = Column(String(255))
    order_id = Column(String(255))
    cancel_time = Column(String(255))
    macd_chart = Column(String(255))
    disparity_chart = Column(String(255))
    option_name = Column(String(255))
    trailingstop_flag = Column(Integer)
    max_price = Column(String(255))


class cp_b_user_t(Base):
    __tablename__ = "cp_b_user_t"

    idx = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Integer)
    name = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    salt = Column(String(255))
    public_key = Column(String(255), default=None)
    secret_key = Column(String(255), default=None)
    search_option = Column(Integer, default=None)
    trading_option = Column(Integer, default=None)
    jwt_token = Column(String(255), default=None)
    refresh_token = Column(String(255), default=None)
