
insertTrandingSql = 'INSERT INTO nc_r_trading_val_t ( daydate, coin_name, coin_end, coin_now, coin_low, coin_high, coin_volumn, coin_fluctate_rate ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

insertTradingLog = 'INSERT INTO nc_r_trading_t (type, coin_name, trading_code, use_coin, order_qty, price, fee, total_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)' 

insertPossessionCoin = 'INSERT INTO nc_r_possession_coin_t (coin, unit, price, total, fee) VALUES(%s, %s, %s, %s, %s)' 

buyUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, price = %s, total = %s, fee = %s WHERE coin = %s'

sellUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, total = %s WHERE coin = %s'

deletePossessionCoin = 'DELETE FROM nc_r_possession_coin_t WHERE coin = %s'

def orderListSql(page, prev):
  return 'SELECT * FROM nc_r_trading_t ORDER BY idx DESC limit ' + page + ' offset ' + prev


def dateOrderListSql(page, prev, dateStart, dateEnd):
  return 'SELECT * FROM nc_r_trading_t  WHERE create_at > ' + dateStart + ' AND create_at < ' + dateEnd + ' ORDER BY idx DESC limit ' + page + ' offset ' + prev 

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_r_trading_t  WHERE create_at > ' + dateStart + ' AND create_at < ' + dateEnd 

orderListCountSql = 'SELECT count(idx) as count FROM nc_r_trading_t'

getMyCoinListSql = 'SELECT * FROM nc_r_possession_coin_t'

def getDBCoinList(price, transaction_price): 
  return 'SELECT coin_name FROM nc_r_coin_list_t WHERE price >= ' + price + ' AND price IS NOT NULL AND transaction_price >= ' + transaction_price

deleteCoinSql = 'SELECT FROM nc_r_coin_list_t WHERE coin_name = %s'

getMASPoptionSql = 'SELECT idx, name, term, color, stroke from nc_b_disparity_option_t'

insetMASPoptionSql = 'INSERT INTO nc_b_disparity_option_t ( name, term, color, stroke ) VALUES ( %s, %s, %s, %s )'

updateMASPoptionSql  = 'UPDATE nc_b_disparity_option_t SET disparity_value = %s, disparity_color = %s WHERE disparity_name = %s'

deleteMASPoptionSql  = 'DELETE FROM nc_b_disparity_option_t WHERE idx = %s'

selectSearchOptionSql = 'SELECT * FROM nc_b_search_option_t'

def selectActiveSearchOptionSql(option_idx): 
  return 'SELECT first_disparity, second_disparity, trends, trends_idx, avg_volume, transaction_amount, price FROM nc_b_search_option_t WHERE idx = ' + option_idx

insertSearchOptionSql = 'INSERT INTO nc_b_search_option_t (name, first_disparity, second_disparity,trends_idx, trends, avg_volume, transaction_amount, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

updateSearchOptionSql = 'UPDATE nc_b_search_option_t SET name = %s , first_disparity = %s , second_disparity = %s ,trends_idx = %s, trends = %s , avg_volume = %s , transaction_amount = %s , price = %s WHERE idx = %s'

selectSearchPriceList = 'SELECT * from nc_f_recommend_coin_t'

insertSearchCoinListSql = 'INSERT INTO nc_f_recommend_coin_t (coin_name, catch_price ) VALUES ( %s, %s )'

deleteSearchCoinListSql = 'DELETE from nc_f_recommend_coin_t'

findUseSearchCondition = 'SELECT * FROM nc_b_search_option_t WHERE used = 1'

findUseTradingCondition = 'SELECT * FROM nc_b_trading_option_t WHERE used = 1'

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
  s.MACD_signal_value 
  from nc_b_trading_option_t op
  left join nc_c_account_option_t ac on op.name = ac.name
  left join nc_c_buy_option_t b on op.name = b.name
  left join nc_c_sell_option_t s on op.name = s.name
  where op.name like ''' + "'" + name + "'"

def getTradingHisSql():
  return ''' select * from nc_p_possession_coin_his_t order by idx desc'''

autoStatusCheck = "SELECT status FROM nc_b_now_auto_status_t"
updateAutoStatus = "UPDATE nc_b_now_auto_status_t SET status = %s WHERE idx = 1"

insertLog = "INSERT INTO nc_f_log_t (content, insert_date) VALUES (%s, now())"