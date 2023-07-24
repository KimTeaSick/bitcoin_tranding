async def transaction_amount_condition(t_condition, minute_max, hour_max):
  if int(t_condition[1]['high_transaction_amount']) == 0:
      print('high_transaction_amount', t_condition[1]['high_transaction_amount'])
      pass
  if t_condition[1]['chart_term'][-1] == 'm' and int(t_condition[1]['chart_term'][:-1]) > minute_max:
      minute_max = int(t_condition[1]['chart_term'][:-1])
  if t_condition[1]['chart_term'][-1] == 'h' and int(t_condition[1]['chart_term'][:-1]) > hour_max:
      hour_max = int(t_condition[1]['chart_term'][:-1])
  return {'option': 'TransactionAmount', 'chart_term': t_condition[1]['chart_term'], 
           'low_transaction_amount': t_condition[1]['low_transaction_amount'], 
           'high_transaction_amount': t_condition[1]['high_transaction_amount']} \
        , minute_max \
        , hour_max