from sql.assetsSql import *

class AssetsFn():
  async def rate_check(self, item, bit, idx):
    try:
      if item.days == '0':
        user_acc_info = []
        day_info = await bit.mysql.Select(get_users_rate_info_sql(idx, 1))
        week_info = await bit.mysql.Select(get_users_rate_info_sql(idx, 7))
        month_info = await bit.mysql.Select(get_users_rate_info_sql(idx, 30))
        account_info = await bit.mysql.Select(account_info_sql(idx))
        user_acc_info.append(day_info[0])
        user_acc_info.append(week_info[0])
        user_acc_info.append(month_info[0])
        print("account_info", account_info)
        return {"account_balance": account_info[-1][1], "rate": 0,
        "date": account_info[0][3][0:8] + " ~ " + account_info[-1][3][0:8],
        "table_data": user_acc_info, "invest_money": account_info[-1][1]}
      else:
        res = 0
        print(str(item.days), str(int(item.days)+1))
        account_info = await bit.mysql.Select(total_rate_sql(str(item.days), idx))
        total_invest = await bit.mysql.Select(total_invest_sql(idx))
        total_withdraw = await bit.mysql.Select(total_withdraw_sql(idx))
        print("total_rate", account_info)
        return {"rate":round(res, 3), "account_balance": account_info[-1][4],
                "date": account_info[0][3][0:8] + " ~ " + account_info[-1][3][0:8],
                "table_data": account_info[::-1], "invest_money": account_info[0][4]}
    except Exception as e:
      print('rate_check Error ::: ::: ', e)