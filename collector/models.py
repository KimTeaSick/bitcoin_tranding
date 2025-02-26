from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class cp_r_coin_list_t(Base):
    __tablename__ = "cp_r_coin_list_t"

    idx = Column(Integer, primary_key=True, index=True)

    coin_name = Column(String(100))
    kr_name = Column(String(100))
    warning = Column(String(100))
    delflag = Column(Integer)

class cp_p_coin_current_candle_price_t(Base):
    __tablename__ = "cp_p_coin_current_candle_price_t"

    coin_name = Column(String(100), primary_key=True)
    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_b_use_search_option_t(Base):
    __tablename__ = "cp_b_use_search_option_t"

    idx = Column(Integer, primary_key=True)

    search_idx = Column(Integer)

class cp_b_disparity_option_t(Base):
    __tablename__ = "cp_b_disparity_option_t"

    disparity_idx = Column(Integer, primary_key=True)
    disparity_name = Column(String(100))
    disparity_color = Column(String(100))
    disparity_value = Column(String(100))

# candle performance ============================================================================================================
class cp_p_min_bithumb_t(Base):
    __tablename__ = "cp_p_min_bithumb_t"

    idx = Column(Integer, primary_key=True, index=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_3min_bithumb_t(Base):
    __tablename__ = "cp_p_3min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_5min_bithumb_t(Base):
    __tablename__ = "cp_p_5min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_10min_bithumb_t(Base):
    __tablename__ = "cp_p_10min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_30min_bithumb_t(Base):
    __tablename__ = "cp_p_30min_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_1H_bithumb_t(Base):
    __tablename__ = "cp_p_1H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    #empty_count = Column(Integer, default=0)

class cp_p_6H_bithumb_t(Base):
    __tablename__ = "cp_p_6H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_12H_bithumb_t(Base):
    __tablename__ = "cp_p_12H_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

class cp_p_1D_bithumb_t(Base):
    __tablename__ = "cp_p_1D_bithumb_t"

    idx = Column(Integer, primary_key=True)

    s_time = Column(Integer)
    open_price = Column(String(100))
    close_price = Column(String(100))
    high_price = Column(String(100))
    low_price = Column(String(100))
    volume = Column(String(100))
    coin_name = Column(String(100))
    time = Column(String(100))
    empty_count = Column(Integer, default=0)

# ==========================================================================================================================================조건 부합 코인 저장


class cp_f_recommend_coin_list_t(Base):
    __tablename__ = "cp_f_recommend_coin_list_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    catch_price = Column(String(100))
    option_name = Column(String(100))

# nmsVersion performance ================================================================================================
class cp_p_coin_current_price_t(Base):
    __tablename__ = "cp_p_coin_current_price_t"

    coin_name = Column(String(100), primary_key=True)

    s_time = Column(Integer)
    time = Column(String(100))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    volume = Column(Float)
    transaction_amount = Column(Float)

class cp_p_1m_coin_price_t(Base):
    __tablename__ = "cp_p_1m_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    s_time = Column(Integer)
    time = Column(String(100))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    ask_price = Column(Float)
    avg_price = Column(Float)
    volume = Column(Float)
    transaction_amount = Column(Float)
    disparity = Column(Float)

class cp_p_30m_coin_price_t(Base):
    __tablename__ = "cp_p_30m_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    s_time = Column(Integer)
    time = Column(String(100))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    ask_price = Column(Float)
    avg_price = Column(Float)
    volume = Column(Float)
    transaction_amount = Column(Float)
    disparity = Column(Float)

class cp_p_1h_coin_price_t(Base):
    __tablename__ = "cp_p_1h_coin_price_t"

    idx = Column(Integer, primary_key=True)

    coin_name = Column(String(100))
    s_time = Column(Integer)
    time = Column(String(100))
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    ask_price = Column(Float)
    avg_price = Column(Float)
    volume = Column(Float)
    transaction_amount = Column(Float)
    disparity = Column(Float)
