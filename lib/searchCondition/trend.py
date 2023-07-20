async def trend_condition(condition, minute_max, hour_max):
  if int(condition[1]['trend_term']) == 0 or int(condition[1]['MASP']) == 0:
    print('trend_term:',
    condition[1]['trend_term'], 'MASP:', condition[1]['MASP'])
    pass
  
  if condition[1]['chart_term'][-1] == 'm' and ((int(condition[1]['trend_term']) + 2 + int(condition[1]['MASP'])) * int(condition[1]['chart_term'][:-1])) > minute_max:
    minute_max = ((int(condition[1]['trend_term']) + 2 + int(condition[1]['MASP'])) * int(condition[1]['chart_term'][:-1]))
    
  if condition[1]['chart_term'][-1] == 'h' and ((int(condition[1]['trend_term']) + 2 + int(condition[1]['MASP'])) * int(condition[1]['chart_term'][:-1])) > hour_max:
    hour_max = ((int(condition[1]['trend_term']) + 2 + int(condition[1]['MASP'])) * int(condition[1]['chart_term'][:-1]))
      
  return ({'option': 'Trend', 'chart_term': condition[1]['chart_term'], 'trend_term': condition[1]['trend_term'],
           'trend_type': condition[1]['trend_type'], 'trend_reverse': condition[1]['trend_reverse'], "MASP": condition[1]['MASP']}) \
           ,minute_max \
           ,hour_max
