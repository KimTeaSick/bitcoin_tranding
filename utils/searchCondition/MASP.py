async def MASP_condition(condition, minute_max, hour_max):
  if int(condition[1]['first_disparity']) == 0 or int(condition[1]['second_disparity']) == 0:
      print('first_disparity: ', condition[1]['first_disparity'], 'second_disparity: ', condition[1]['second_disparity'])
      pass
   
  bigger = int(condition[1]['first_disparity']) \
  if int(condition[1]['first_disparity']) > int(condition[1]['second_disparity']) \
  else int(condition[1]['second_disparity'])


  if condition[1]['chart_term'][-1] == 'm' and bigger * int(condition[1]['chart_term'][:-1]) > minute_max:
      minute_max = bigger * int(condition[1]['chart_term'][:-1])

  if condition[1]['chart_term'][-1] == 'h' and (bigger * int(condition[1]['chart_term'][:-1])) > hour_max:
      hour_max = bigger * int(condition[1]['chart_term'][:-1])
  
  return {'option': 'MASP', 'chart_term': condition[1]['chart_term'], 'first_disparity': condition[1]['first_disparity'], 
           'second_disparity': condition[1]['second_disparity'], 'comparison': condition[1]['comparison']}\
           ,minute_max \
           ,hour_max