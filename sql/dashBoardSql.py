getMyCoinListSql = 'SELECT * FROM nc_r_possession_coin_t'

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd 