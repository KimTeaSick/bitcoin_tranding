async def MACD_condition(condition, minute_max, hour_max ):
  if int(condition[1]['short_disparity']) == 0 or int(condition[1]['long_disparity']) == 0:
      print('short_disparity:', condition[1]['short_disparity'], 'long_disparity:', condition[1]['long_disparity'])
      pass
  
  if condition[1]['chart_term'][-1] == 'm' and ((int(condition[1]['long_disparity']) * 2 + int(condition[1]['signal'])) * int(condition[1]['chart_term'][:-1])) > minute_max:
      minute_max = (int(condition[1]['long_disparity']) * 2 + int(condition[1]['signal'])) * int(condition[1]['chart_term'][:-1])

  if condition[1]['chart_term'][-1] == 'h' and ((int(condition[1]['long_disparity']) * 2 + int(condition[1]['signal'])) * int(condition[1]['chart_term'][:-1])) > hour_max:
      hour_max = (int(condition[1]['long_disparity']) * 2 + int(condition[1]['signal'])) * int(condition[1]['chart_term'][:-1])

  return ({'option': 'MACD', 'chart_term': condition[1]['chart_term'], 'short_disparity': condition[1]['short_disparity'],
           'long_disparity': condition[1]['long_disparity'], 'signal': condition[1]['signal'], 'up_down': condition[1]['up_down']}) \
        ,minute_max \
        ,hour_max