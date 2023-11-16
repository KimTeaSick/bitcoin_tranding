async def disparity_condition(condition, minute_max, hour_max):
  if int(condition[1]['disparity_term']) == 0:
    print('disparity_term:', condition[1]['disparity_term'])
    pass
  
  if condition[1]['chart_term'][-1] == 'm':
    if (int(condition[1]['disparity_term']) * int(condition[1]['chart_term'][:-1])) > minute_max:
      minute_max = int(condition[1]['disparity_term']) * int(condition[1]['chart_term'][:-1])
          
  if condition[1]['chart_term'][-1] == 'h':
    if (int(condition[1]['disparity_term']) * int(condition[1]['chart_term'][:-1])) > hour_max:
      hour_max = (int(condition[1]['disparity_term']) * int(condition[1]['chart_term'][:-1]))
          
  return {'option': 'Disparity', 'chart_term': condition[1]['chart_term'], 
           'disparity_term': condition[1]['disparity_term'], 'low_disparity': int(condition[1]['low_disparity']), 
           'high_disparity': int(condition[1]['high_disparity'])}, minute_max, hour_max
