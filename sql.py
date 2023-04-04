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

getDisparityOptionSql = 'SELECT option_name, option_value, option_color from nc_b_option_t WHERE option_name = "line_one" or option_name = "line_two" or option_name = "line_three"'

updateDisparityOptionSql = 'UPDATE nc_b_option_t SET option_value = %s, option_color = %s WHERE option_name = %s'

insertSearchOptionSql = 'INSERT INTO nc_b_search_option_t (name, first_disparity, second_disparity, trends, avg_volume, transaction_amount, price) VALUES (%s, %s, %s, %s, %s, %s, %s)'

updateSearchOptionSql = 'UPDATE nc_b_search_option_t SET name = %s , first_disparity = %s , second_disparity = %s , trends = %s , avg_volume = %s , transaction_amount = %s , price = %s '