getMyCoinListSql = 'SELECT * FROM nc_r_possession_coin_t'

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd 

def total_rate_sql(days):
  return f'SELECT rate, account_balance FROM nc_r_account_rate_t order by insert_date DESC limit {days}'