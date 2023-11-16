getMemberListSql = '''
select
	user.name,
	user.email,
	user.active,
	user.start_date,
	acc.account_balance,
  user.idx
from 
	nc_b_user_t user
	left join (
	select account_balance,
	user_idx
	from nc_r_account_rate_t 
	where insert_date = date_sub(current_date, interval 0 day)
	) acc on user.idx = acc.user_idx
  '''