def getMyCoinListSql(idx): return f'SELECT * FROM nc_r_possession_coin_t WHERE user_idx = {idx} AND status != 1'

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd 

def total_rate_sql(days, idx):
  return f'SELECT rate, account_balance FROM nc_r_account_rate_t WHERE user_idx = {idx} order by insert_date DESC limit {days}'