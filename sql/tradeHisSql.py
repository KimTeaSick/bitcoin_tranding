def orderListCountSql(idx):
  return f'SELECT count(idx) as count FROM nc_p_possession_coin_his_t WHERE user_idx = {idx}'

def orderListSql(idx, page, prev):
  return 'SELECT coin, unit, price, total, fee, type, transaction_time FROM nc_p_possession_coin_his_t WHERE user_idx = ' + idx + ' ORDER BY idx DESC limit ' + page + ' offset ' + prev

def dateOrderListSql(page, prev, dateStart, dateEnd):
  return 'SELECT * FROM nc_p_possession_coin_his_t  WHERE transaction_time > ' + dateStart + ' AND transaction_time < ' + dateEnd + ' ORDER BY idx DESC limit ' + page + ' offset ' + prev 
