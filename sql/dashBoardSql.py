def getMyCoinListSql(idx): return f'SELECT * FROM nc_r_possession_coin_t WHERE user_idx = {idx} AND status != 1'

def todayOrderListSql(dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd 

def total_rate_sql(days, idx):
  return f'''
  SELECT rate, account_balance, invest, insert_date, revenue
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

def users_info_sql(idx):
  return f'''
    SELECT name
    FROM nc_b_user_t
    WHERE idx = {idx}
  '''

def users_total_acc_sql(idx):
  return f'''
    SELECT account_balance
    FROM nc_r_account_rate_t
    WHERE user_idx = {idx}
    ORDER BY idx DESC LIMIT 1
  '''

def get_user_acc_info(idx, day):
  return f'''
    select 
      account_balance,
      revenue,
      rate
    from 
      nc_r_account_rate_t 
    where 
      insert_date = DATE_SUB(CURRENT_DATE , INTERVAL {day} day)
    and 
      user_idx = {idx}
  '''

def max_day_acc_info(idx):
  return f'''
    select 
      account_balance,
      insert_date,
      user_idx
    from 
      nc_r_account_rate_t 
    where 
      insert_date = (
        select min(insert_date) 
        from nc_r_account_rate_t 
        where user_idx = {idx}
      ) 
      and user_idx = {idx}
'''

def day_data_sql(idx):
  return f'''
    SELECT
      account_balance AS total_value,
      revenue,
      rate
    FROM
      nc_r_account_rate_t
    WHERE user_idx = {idx}
    ORDER BY insert_date DESC LIMIT 7
    '''

def day_end_acc_sql(idx, date):
  return f'''
    select 
      account_balance,
      insert_date
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE, INTERVAL {date} day)
      and user_idx = {idx}
'''

def day_start_acc_sql(idx, date):
  return f'''
    select 
      account_balance,
      insert_date
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE , INTERVAL {date + 1} day)
      and user_idx = {idx}
'''











def week_avg_data_sql(idx, date):
  return f'''
    select 
      sum(account_balance)/count(account_balance) as week_balance_total,
      sum(revenue) week_revenue_total
    from nc_r_account_rate_t 
    where
      insert_date <= DATE_SUB(CURRENT_DATE, INTERVAL {date} week)
      and insert_date >= DATE_ADD(DATE_SUB(CURRENT_DATE , INTERVAL {date + 1} week), INTERVAL 1 day)
      and user_idx = {idx}
'''

def week_end_acc_sql(idx, date):
  return f'''
    select 
      account_balance,
      insert_date
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE, INTERVAL {date} week)
      and user_idx = {idx}
'''

def week_start_acc_sql(idx, date):
  return f'''
    select 
      account_balance,
      insert_date
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE , INTERVAL {date + 1} week)
      and user_idx = {idx}
'''

def month_end_acc_sql(idx, date):
  return f'''
    select 
      account_balance
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE, INTERVAL {date} month)
      and user_idx = {idx}
'''

def month_start_acc_sql(idx, date):
  return f'''
    select 
      account_balance
    from nc_r_account_rate_t 
    where
      insert_date = DATE_SUB(CURRENT_DATE , INTERVAL {date + 1} month)
      and user_idx = {idx}
    '''

def month_avg_data_sql(idx, date):
  return f'''
    select 
      sum(account_balance) / count(account_balance) as week_balance_total,
      sum(revenue) as month_revenue_total
    from nc_r_account_rate_t 
    where
      insert_date <= DATE_SUB(CURRENT_DATE, INTERVAL {date} MONTH)
      and insert_date >= DATE_SUB(CURRENT_DATE , INTERVAL {date + 1} MONTH)
      and user_idx = {idx}
    '''

def his_data_sql(idx, date):
  return f'''
    SELECT coin, unit, price, total, fee,transaction_time, type, sell_reason
    FROM nc_p_possession_coin_his_t
    WHERE user_idx = {idx} 
    AND transaction_time > '{date}'
    ORDER BY transaction_time DESC
    '''

def getWithdrawSql(idx, day):
  return f'''
    select withdraw 
    from nc_r_account_rate_t 
    where user_idx = {idx}
    and insert_date >= DATE_SUB(CURRENT_DATE , INTERVAL {day} day)
  '''

def getInvestSql(idx, day):
  return f'''
    select invest 
    from nc_r_account_rate_t 
    where user_idx = {idx}
    and insert_date >= DATE_SUB(CURRENT_DATE , INTERVAL {day} day)
  '''

def getTotalOperateMoneySql(date): 
  return f'''
  select sum(account_balance)
  from nc_r_account_rate_time_t
  where insert_date >= {date}
  '''

def getDateDataSql(idx):
  return f'''
    select 
      insert_date
    from nc_r_account_rate_t 
    where
      insert_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 week)
      and user_idx = {idx}
'''

def getChartDataSql(idx):
  return f'''
    select 
      account_balance
    from nc_r_account_rate_t 
    where
      insert_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 month)
      and user_idx = {idx}
'''

getUserCountSql = """
select count(idx) from nc_b_user_t
"""

def getTableUserList(now): 
  return f"""select user.idx 
	from 
	nc_b_user_t user
	left join (
	select account_balance,
	user_idx
	from nc_r_account_rate_t 
	where insert_date = date_sub(current_date, interval 0 day)
	) acc on user.idx = acc.user_idx
	order by acc.account_balance DESC
	limit 3 offset {(now - 1) * 3}"""