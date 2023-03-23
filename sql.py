insertTrandingSql = 'INSERT INTO nc_r_trading_val_t ( daydate, coin_name, coin_end, coin_now, coin_low, coin_high, coin_volumn, coin_fluctate_rate ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

insertTradingLog = 'INSERT INTO nc_r_trading_t (type, coin_name, trading_code, use_coin, order_qty, price, fee, total_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)' 

insertPossessionCoin = 'INSERT INTO nc_r_possession_coin_t (coin, unit, price, total, fee) VALUES(%s, %s, %s, %s, %s)' 

buyUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, price = %s, total = %s, fee = %s WHERE coin = %s'

sellUpdatePossessionCoin = 'UPDATE nc_r_possession_coin_t SET unit = %s, total = %s WHERE coin = %s'

deletePossessionCoin = 'DELETE FROM nc_r_possession_coin_t WHERE coin = %s'

def orderListSql(page, prev):
  return 'SELECT * FROM nc_r_trading_t ORDER BY idx DESC limit ' + page + ' offset ' + prev

orderListCountSql = 'SELECT count(idx) as count FROM nc_r_trading_t'

def dashOrderListSql():
  return 'select * from( select * from tb_test where (code, date_time) in ( select code, max(date_time) as date_time from tb_test group by code ) order by date_time desc ) t group by t.code'

getMyCoinListSql = 'select * from nc_r_possession_coin_t'
