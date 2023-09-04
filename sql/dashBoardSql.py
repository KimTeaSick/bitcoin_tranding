def getMyCoinListSql(idx): return f'SELECT * FROM nc_r_possession_coin_t WHERE user_idx = {idx} AND status != 1'

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd 

def total_rate_sql(days, idx):
  return f'''
  SELECT rate, account_balance, invest, insert_date 
  FROM nc_r_account_rate_t 
  WHERE user_idx = {idx} order by insert_date DESC limit 1, {days}
'''

def total_invest_sql(idx):
  return f'''
  SELECT sum(invest)
  FROM nc_r_account_rate_t 
  WHERE user_idx = {idx}
'''

def total_withdraw_sql(idx):
  return f'''
  SELECT sum(withdraw)
  FROM nc_r_account_rate_t 
  WHERE user_idx = {idx}
'''