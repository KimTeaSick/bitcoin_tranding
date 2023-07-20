from .price import price_condition
from .transactionAmount import transaction_amount_condition
from .MASP import MASP_condition
from .MACD import MACD_condition
from .disparity import disparity_condition
from .trend import trend_condition

async def option_standardization(item):
  use_option_list = []
  options = []
  max_minute = 0
  max_hour = 0
  # print("getRecommendCoin item ::::::: ", item)
  # 사용 옵션 확인 및 변환
  for condition in item:
    if condition[1]['flag'] != 0:
      use_option_list.append(condition[0])
      if condition[0] == 'Price':
        price_return = await price_condition(condition, max_minute)
        print("price_return ::::::: --------------------------- ", price_return)
        options.append(price_return[0])
        max_minute = price_return[1]
      if condition[0] == 'TransactionAmount':
        t_return = await transaction_amount_condition(condition, max_minute, max_hour)
        options.append(t_return[0])
        max_minute = t_return[1]
        max_hour = t_return[2]
      if condition[0] == 'MASP':
        M_return = await MASP_condition(condition, max_minute, max_hour)
        options.append(M_return[0])
        max_minute = M_return[1]
        max_hour = M_return[2]
      if condition[0] == 'Disparity':
        d_return = await disparity_condition(condition, max_minute, max_hour)
        options.append(d_return[0])
        max_minute = d_return[1]
        max_hour = d_return[2]
      if condition[0] == 'Trend':
        trend_return = await trend_condition(condition, max_minute, max_hour)
        options.append(trend_return[0])
        max_minute = trend_return[1]
        max_hour = trend_return[2]
      if condition[0] == 'MACD':
        MACD_retrun = await MACD_condition(condition, max_minute, max_hour)
        options.append(MACD_retrun[0])
        max_minute = MACD_retrun[1]
        max_hour = MACD_retrun[2]

  return use_option_list, options, max_minute, max_hour