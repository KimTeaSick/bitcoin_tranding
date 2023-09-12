def total_rate_sql(days, idx):
  return f'''
  SELECT rate, revenue, invest, insert_date, account_balance
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

def get_users_rate_info_sql(idx, day):
  return f'''
  SELECT SUM(rate), sum(revenue)
  FROM (
    SELECT rate, revenue
    FROM nc_r_account_rate_t
    WHERE user_idx = {idx}
    ORDER BY idx DESC LIMIT {day}
  ) AS top_7_sales;
  '''

def account_info_sql(idx):
  return f'''
    SELECT rate, account_balance, invest, insert_date, revenue
    FROM nc_r_account_rate_t
    WHERE user_idx = {idx}
    '''