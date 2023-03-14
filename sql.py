insertTrandingSql = 'INSERT INTO nc_r_trading_val_t ( daydate, coin_name, coin_end, coin_now, coin_low, coin_high, coin_volumn, coin_fluctate_rate ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

insertTradingLog = 'INSERT INTO nc_r_trading_t (trading_code, type, coin_name, use_coin) VALUES(%s, %s, %s, %s)' 

def orderListSql(page, prev):
  return 'SELECT * FROM nc_r_trading_t ORDER BY idx DESC limit ' + page + ' offset ' + prev

orderListCountSql = 'SELECT count(idx) as count FROM nc_r_trading_t'