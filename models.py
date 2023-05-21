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
    idx = Column(Integer)
    name = Column(String(100), primary_key=True)

    Price = Column(Integer)
    Transaction_amount = Column(Integer)
    MASP = Column(Integer)
    Disparity = Column(Integer)
    Trend = Column(Integer)
    MACD = Column(Integer)
    Create_date = Column(String(100))
    Update_date = Column(String(100))
    used = Column(Integer)

class PriceOption(Base):
    __tablename__ = "nc_c_pr_price_t"
    idx = Column(Integer, primary_key=True, index=True)
    low_price = Column(Integer)
    high_price = Column(Integer)

class TransactionAmountOption(Base):
    __tablename__ = "nc_c_pr_transaction_amount_t"
    idx = Column(Integer, primary_key=True, index=True)
    low_transaction_amount = Column(Integer)
    high_transaction_amount = Column(Integer)
    

class MASPOption(Base):
    __tablename__ = "nc_c_masp_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    first_disparity = Column(Integer)
    second_disparity = Column(Integer)
    comparison = Column(String(100))

class DisparityOption(Base):
    __tablename__ = "nc_c_disparity_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    disparity_term = Column(String(100))
    low_disparity = Column(Integer)
    high_disparity = Column(Integer)

class TrendOption(Base):
    __tablename__ = "nc_c_trend_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    MASP = Column(Integer)
    trend_term = Column(Integer)
    trend_reverse = Column(Integer)
    trend_type = Column(String(100))

class MACDOption(Base):
    __tablename__ = "nc_c_macd_t"
    idx = Column(Integer, primary_key=True, index=True)
    chart_term = Column(String(100))
    short_disparity = Column(Integer)
    long_disparity = Column(Integer)
    up_down = Column(String(100))

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
    empty_count = Column(Integer, default=0)

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
class recommandT(Base):
    __tablename__ = "nc_f_recommend_coin_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    catch_price = Column(String(100))
    option_name = Column(String(100))

class recommandList(Base):
    __tablename__ = "nc_f_recommend_coin_list_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    catch_price = Column(String(100))
    option_name = Column(String(100))

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