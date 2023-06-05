from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class coinList(Base):
    __tablename__ = "nc_r_coin_list_t"

    idx = Column(Integer, primary_key=True, index=True)

    coin_name = Column(String(100))
    kr_name = Column(String(100))
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

class usedOption(Base):
    __tablename__ = "nc_b_use_search_option_t"

    idx = Column(Integer, primary_key=True)

    search_idx = Column(Integer)

class disparityOption(Base):
    __tablename__ = "nc_b_disparity_option_t"

    disparity_idx = Column(Integer, primary_key=True)
    disparity_name = Column(String(100))
    disparity_color = Column(String(100))
    disparity_value = Column(String(100))

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
    #empty_count = Column(Integer, default=0)

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
    transaction_amount = Column(Float)
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

'''
# options ============================================================================================================

class conditions(Base):
    __tablename__ = "nc_b_condition"

    idx = Column(Integer, primary_key=True)

    group_idx = Column(Integer)
    condition_name = Column(Integer)
    use_option = Column(Integer)

class options(Base):
    __tablename__ = "nc_b_search_option_t"

    idx = Column(Integer, primary_key=True)

    name = Column(String(100))
    pr_price = Column(Integer)
    pr_fluctuation = Column(Integer)
    pr_transaction_amount = Column(Integer)
    MASP_comparison = Column(Integer)
    MASP_comparison_double = Column(Integer)
    MASP_disparity = Column(Integer)
    MASP_trend = Column(Integer)
    v_volume = Column(Integer)
    v_avg_volume = Column(Integer)
    D_over_RV = Column(Integer)
    D_range_RV = Column(Integer)
    D_range_RV_up_down = Column(Integer)
    D_trend = Column(Integer)
    D_reverse = Column(Integer)
    MACD_line_over = Column(Integer)
    MACD_line_comparison = Column(Integer)
    MACD_value_over = Column(Integer)
    MACD_value_up_down = Column(Integer)
    MACD_value_range = Column(Integer)
    MACD_trend = Column(Integer)
    MACD_reverse = Column(Integer)
    MACDS_value_over = Column(Integer)
    MACDS_value_up_down = Column(Integer)
    MACDS_value_range = Column(Integer)
    MACDS_trend = Column(Integer)
    MACDS_reverse = Column(Integer)

#==========================================================================================================================================조건 테이블

class useP_fluctuationType(Base):
  __tablename__ = "nc_c_pr_fluctuation_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  prev = Column(Integer)
  now = Column(Integer)
  percent = Column(Integer)

class useP_rangeType(Base):
  __tablename__ = "nc_c_pr_price_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  first_value = Column(Integer)
  second_value = Column(Integer)

class useP_transactionAmount(Base):
  __tablename__ = "nc_c_pr_transaction_amount_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  first = Column(Integer)
  second = Column(Integer)

class useV_volume(Base):
  __tablename__ = "nc_c_v_volume_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  first = Column(Integer)
  second = Column(Integer)

class useV_avg_volumeType(Base):
  __tablename__ = "nc_c_v_avg_volume_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  recent = Column(Integer)
  first = Column(Integer)
  second = Column(Integer)

class useMASP_comparisonType(Base):
  __tablename__ = "nc_c_masp_comparison_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  first = Column(Integer)
  second = Column(Integer)
  range = Column(Integer)
  percent = Column(Integer)

class useMASP_comparison_doubleType(Base):
  __tablename__ = "nc_c_masp_comparison_double_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  first_disparity_first_value = Column(Integer)
  first_comparision = Column(String(100))
  first_disparity_second_value = Column(Integer)
  second_disparity_first_value = Column(Integer)
  second_comparision = Column(String(100))
  second_disparity_second_value = Column(Integer)

class useMASP_disparityType(Base):
  __tablename__ = "nc_c_masp_disparity_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  first_disparity = Column(Integer)
  second_disparity = Column(Integer)
  percent = Column(Integer)

class useMASP_trendType(Base):
  __tablename__ = "nc_c_masp_trend_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  disparity_term = Column(Integer)
  trend_type = Column(String(100))
  trend_term = Column(Integer)

class useD_overRVType(Base):
  __tablename__ = "nc_c_d_over_rv_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  disparity_term = Column(Integer)
  disparity_value = Column(Integer)
  trend_type = Column(String(100))

class useD_rangeRVType(Base):
  __tablename__ = "nc_c_d_range_rv_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  range = Column(Integer)
  firstRange_value = Column(Integer)
  secondRange_value = Column(Integer)

class useD_RV_up_downType(Base):
  __tablename__ = "nc_c_d_range_rv_up_down_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  range = Column(Integer)
  disparity_value = Column(Integer)
  up_down = Column(String(100))

class useD_trendType(Base):
  __tablename__ = "nc_c_d_trend_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  range = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))

class useD_reverseType(Base):
  __tablename__ = "nc_c_d_reverse_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  range = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))

class useMACD_line_overType(Base):
  __tablename__ = "nc_c_macd_line_over_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  line_over = Column(String(100))

class useMACD_line_comparisonType(Base):
  __tablename__ = "nc_c_macd_line_comparison_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  line_comparison = Column(String(100))

class useMACD_value_overType(Base):
  __tablename__ = "nc_c_macd_value_over_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  value = Column(Integer)
  value_over_type = Column(String(100))

class useMACD_value_up_downType(Base):
  __tablename__ = "nc_c_macd_value_up_down_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  value = Column(Integer)
  value_up_down = Column(String(100))

class useMACD_value_rangeType(Base):
  __tablename__ = "nc_c_macd_value_range_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  value_range_one = Column(Integer)
  value_range_two = Column(Integer)

class useMACD_trendType(Base):
  __tablename__ = "nc_c_macd_trend_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))

class useMACD_reverseType(Base):
  __tablename__ = "nc_c_macd_reverse_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))

class useMACDS_value_overType(Base):
  __tablename__ = "nc_c_macds_value_over_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  value = Column(Integer)
  value_over_type = Column(String(100))

class useMACDS_value_up_downType(Base):
  __tablename__ = "nc_c_macds_value_up_down_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  value = Column(Integer)
  value_up_down = Column(String(100))

class useMACDS_value_rangeType(Base):
  __tablename__ = "nc_c_macds_value_range_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  value_range_one = Column(Integer)
  value_range_two = Column(Integer)

class useMACDS_trendType(Base):
  __tablename__ = "nc_c_macds_trend_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))

class useMACDS_reverseType(Base):
  __tablename__ = "nc_c_macds_reverse_t"

  idx = Column(Integer, primary_key=True)

  term = Column(String(100))
  timeing = Column(Integer)
  shot = Column(Integer)
  long = Column(Integer)
  signal = Column(Integer)
  trend_term = Column(Integer)
  trend_type = Column(String(100))
'''