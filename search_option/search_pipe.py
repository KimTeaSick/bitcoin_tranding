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

def raw_search_pipe(value):
  print("raw_search_pipe :::: ", value)
  print("raw_search_pipe :::: ", value.Price['flag'])

  R_VALUE = {
  "p_low_price": str(value.Price['low_price']),
  "p_high_price": str(value.Price['high_price']),
  "p_flag": str(value.Price['flag']),
  "ta_chart_term": str(value.TransactionAmount['chart_term']),
  "ta_low_transaction_amount": str(value.TransactionAmount['low_transaction_amount']),
  "ta_high_transaction_amount": str(value.TransactionAmount['high_transaction_amount']),
  "ta_flag": str(value.TransactionAmount['flag']),
  "masp_chart_term": str(value.MASP['chart_term']),
  "masp_first_disparity": str(value.MASP['first_disparity']),
  "masp_comparison": str(value.MASP['comparison']),
  "masp_second_disparity": str(value.MASP['second_disparity']),
  "masp_flag": str(value.MASP['flag']),
  "t_chart_term": str(value.Trend['chart_term']),
  "t_MASP": str(value.Trend['MASP']),
  "t_trend_term": str(value.Trend['trend_term']),
  "t_trend_type": str(value.Trend['trend_type']),
  "t_trend_reverse": str(value.Trend['trend_reverse']),
  "t_flag": str(value.Trend['flag']),
  "d_chart_term": str(value.Disparity['chart_term']),
  "d_disparity_term": str(value.Disparity['disparity_term']),
  "d_low_disparity": str(value.Disparity['low_disparity']),
  "d_high_disparity": str(value.Disparity['high_disparity']),
  "d_flag": str(value.Disparity['flag']),
  "macd_chart_term": str(value.MACD['chart_term']),
  "macd_short_disparity": str(value.MACD['short_disparity']),
  "macd_long_disparity": str(value.MACD['long_disparity']),
  "macd_signal": str(value.MACD['signal']),
  "macd_up_down": str(value.MACD['up_down']),
  "macd_flag": str(value.MACD['flag']),
  }

  return R_VALUE

def getCondition(db, models, idx):
  user = db.query(models.USER_T).filter(models.USER_T.idx == idx).first()
  priceCondiotion = db.query(models.nc_c_pr_price).filter(models.nc_c_pr_price == user.search_option).first()
  print('priceCondiotion')
  return priceCondiotion