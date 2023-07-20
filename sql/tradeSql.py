selectSearchPriceList = 'SELECT * from nc_f_recommend_coin_t'

findUseTradingCondition = 'SELECT * FROM nc_b_trading_option_t WHERE used = 1'

def getTradingHisSql():
  return "SELECT * FROM nc_p_possession_coin_his_t WHERE transaction_time >= (SELECT start_date FROM nc_b_now_auto_status_t) order by idx desc"

def useSearchOptionStatus(name):
  return '''
  select 
  op.name,
  p.low_price,
  p.high_price,
  ta.chart_term,
  ta.low_transaction_amount,
  ta.high_transaction_amount,
  masp.chart_term,
  masp.first_disparity,
  masp.comparison,
  masp.second_disparity,
  t.chart_term,
  t.MASP,
  t.trend_term,
  t.trend_type,
  t.trend_reverse,
  d.chart_term,
  d.disparity_term,
  d.low_disparity,
  d.high_disparity,
  macd.chart_term,
  macd.short_disparity,
  macd.long_disparity,
  macd.signal,
  macd.up_down
  from nc_b_search_option_t op
  left join nc_c_pr_price_t p on p.name = op.name and p.flag = 1
  left join nc_c_pr_transaction_amount_t ta on ta.name = op.name and ta.flag = 1
  left join nc_c_masp_t masp on masp.name = op.name and masp.flag = 1
  left join nc_c_trend_t t on t.name = op.name and t.flag = 1
  left join nc_c_disparity_t d on d.name = op.name and d.flag = 1
  left join nc_c_macd_t macd on macd.name = op.name and macd.flag = 1
  where op.name like ''' + "'" + name + "'"

def useTradingOptionStatus(name):
  return '''
  select 
  op.name,
  ac.price_count,
  ac.loss_cut_under_percent,
  ac.loss_cut_under_call_price_sell_all,
  ac.loss_cut_under_coin_specific_percent,
  ac.loss_cut_under_call_price_specific_coin,
  ac.loss_cut_over_percent,
  ac.loss_cut_over_call_price_sell_all,
  ac.loss_cut_over_coin_specific_percent,
  ac.loss_cut_over_call_price_specific_coin,
  ac.buy_cancle_time,
  ac.sell_cancle_time,
  b.percent_to_buy_method,
  b.price_to_buy_method,
  b.callmoney_to_buy_method,
  s.upper_percent_to_price_condition,
  s.down_percent_to_price_condition,
  s.disparity_for_upper_case,
  s.upper_percent_to_disparity_condition,
  s.disparity_for_down_case,
  s.down_percent_to_disparity_condition ,
  s.call_money_to_sell_method ,
  s.percent_to_split_sell ,
  s.shot_MACD_value ,
  s.long_MACD_value ,
  s.MACD_signal_value,
  s.trailing_start_percent,
  s.trailing_stop_percent,
  s.trailing_order_call_price
  from nc_b_trading_option_t op
  left join nc_c_account_option_t ac on op.name = ac.name
  left join nc_c_buy_option_t b on op.name = b.name
  left join nc_c_sell_option_t s on op.name = s.name
  where op.name like ''' + "'" + name + "'"

getATOrderList = 'SELECT * FROM nc_r_order_coin_t'

updateAutoStatus = "UPDATE nc_b_now_auto_status_t SET status = %s, start_date = %s WHERE idx = 1"