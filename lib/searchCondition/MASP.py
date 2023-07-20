async def MASP_condition(M_condition, minute_max, hour_max):
  if int(M_condition[1]['first_disparity']) == 0 or int(M_condition[1]['second_disparity']) == 0:
      print('first_disparity: ', M_condition[1]['first_disparity'], 'second_disparity: ', M_condition[1]['second_disparity'])
      pass
  
  bigger = int(M_condition[1]['first_disparity']) \
  if int(M_condition[1]['first_disparity']) > int(M_condition[1]['second_disparity']) \
  else int(M_condition[1]['second_disparity'])


  if M_condition[1]['chart_term'][-1] == 'm' and bigger * int(M_condition[1]['chart_term'][:-1]) > minute_max:
      minute_max = bigger * int(M_condition[1]['chart_term'][:-1])

  if M_condition[1]['chart_term'][-1] == 'h' and (bigger * int(M_condition[1]['chart_term'][:-1])) > hour_max:
      hour_max = bigger * int(M_condition[1]['chart_term'][:-1])
  
  return ({'option': 'MASP', 'chart_term': M_condition[1]['chart_term'], 'first_disparity': M_condition[1]['first_disparity'], 
           'second_disparity': M_condition[1]['second_disparity'], 'comparison': M_condition[1]['comparison']})\
           ,minute_max \
           ,hour_max