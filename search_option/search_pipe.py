SEARCH_CONDITION_LIST = [
  "p_low_price",
  "p_high_price",
  "p_flag",
  "ta_chart_term",
  "ta_low_transaction_amount",
  "ta_high_transaction_amount",
  "ta_flag",
  "masp_chart_term",
  "masp_first_disparity",
  "masp_comparison",
  "masp_second_disparity",
  "masp_flag",
  "t_chart_term",
  "t_MASP",
  "t_trend_term",
  "t_trend_type",
  "t_trend_reverse",
  "t_flag",
  "d_chart_term",
  "d_disparity_term",
  "d_low_disparity",
  "d_high_disparity",
  "d_flag",
  "macd_chart_term",
  "macd_short_disparity",
  "macd_long_disparity",
  "macd_signal",
  "macd_up_down",
  "macd_flag",
]

def search_pipe(value):
  R_VALUE = {}
  for element in range(len(SEARCH_CONDITION_LIST)):
    R_VALUE[SEARCH_CONDITION_LIST[element]] = str(value[element])

  return R_VALUE