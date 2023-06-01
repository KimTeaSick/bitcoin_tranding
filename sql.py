insertTrandingSql = 'INSERT INTO nc_r_trading_val_t ( daydate, coin_name, coin_end, coin_now, coin_low, coin_high, coin_volumn, coin_fluctate_rate ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
insertTradingLog = 'INSERT INTO nc_r_trading_t (type, coin_name, trading_code, use_coin, order_qty, price, fee, total_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)' 

insertPossessionCoin = 'INSERT INTO nc_r_possession_coin_t (coin, unit, price, total, fee) VALUES(%s, %s, %s, %s, %s)' 
buyUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, price = %s, total = %s, fee = %s WHERE coin = %s'
sellUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, total = %s WHERE coin = %s'
deletePossessionCoin = "DELETE FROM nc_r_possession_coin_t WHERE coin = %s"
def getPossessionCoin(coin):
  return "SELECT * FROM nc_r_possession_coin_t WHERE coin = '" + coin + "'"

def orderListSql(page, prev):
  return 'SELECT * FROM nc_r_trading_t ORDER BY idx DESC limit ' + page + ' offset ' + prev
def dateOrderListSql(page, prev, dateStart, dateEnd):
  return 'SELECT * FROM nc_r_trading_t  WHERE create_at > ' + dateStart + ' AND create_at < ' + dateEnd + ' ORDER BY idx DESC limit ' + page + ' offset ' + prev 
def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_r_trading_t  WHERE create_at > ' + dateStart + ' AND create_at < ' + dateEnd 
orderListCountSql = 'SELECT count(idx) as count FROM nc_r_trading_t'

getMyCoinListSql = 'SELECT * FROM nc_r_possession_coin_t'
deleteCoinSql = 'SELECT FROM nc_r_coin_list_t WHERE coin_name = %s'
def getDBCoinList(price, transaction_price): 
  return 'SELECT coin_name FROM nc_r_coin_list_t WHERE price >= ' + price + ' AND price IS NOT NULL AND transaction_price >= ' + transaction_price

getDisparityOptionSql = 'SELECT disparity_idx, disparity_name, disparity_value, disparity_color from nc_b_disparity_option_t WHERE disparity_name = "line_one" or disparity_name = "line_two" or disparity_name = "line_three"'
updateDisparityOptionSql  = 'UPDATE nc_b_disparity_option_t SET disparity_value = %s, disparity_color = %s WHERE disparity_name = %s'

selectSearchOptionSql = 'SELECT * FROM nc_b_search_option_t'
selectUseSearchOptionSql = 'SELECT search_idx FROM nc_b_use_search_option_t'
insertSearchOptionSql = 'INSERT INTO nc_b_search_option_t (name, first_disparity, second_disparity,trends_idx, trends, avg_volume, transaction_amount, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
updateSearchOptionSql = 'UPDATE nc_b_search_option_t SET name = %s , first_disparity = %s , second_disparity = %s ,trends_idx = %s, trends = %s , avg_volume = %s , transaction_amount = %s , price = %s WHERE idx = %s'
updateUseSearchOption = 'UPDATE nc_b_use_search_option_t SET search_idx = %s '
def selectActiveSearchOptionSql(option_idx): 
  return 'SELECT first_disparity, second_disparity, trends, trends_idx, avg_volume, transaction_amount, price FROM nc_b_search_option_t WHERE idx = ' + option_idx

insertRecommendCoin = 'Insert into nc_f_recommend_coin_t (coin_name, catch_price) values (%s, %s)'
selectRecommendCoin = 'Select * from nc_f_recommend_coin_t'
deleteRecommendCoin = 'DELETE FROM nc_f_recommend_coin_t'

insertLog = 'INSERT INTO nc_b_log_t (log_idx, log_content) VALUES (%s, %s)'

def selectWarningFlag(coin_name): 
  return 'Select warning from nc_r_coin_list_t WHERE coin_name = ' + "'" + coin_name + "'" 

updateWarningFlag = 'UPDATE nc_r_coin_list_t SET warning = %s WHERE coin_name = %s'

getConditionList = 'SELECT a.idx, a.group_idx, b.group_name, a.condition_name FROM nc_b_condition a LEFT JOIN nc_b_condition_group b ON a.group_idx = b.idx'
getConditionGroupList = 'SELECT * FROM nc_b_condition_group'