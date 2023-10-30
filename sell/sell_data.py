def get_active_user(db, models):
  try:
    # return db.query(models.USER_T).filter(models.USER_T.active == 1).all()
    return db.query(models.USER_T).all()
  except:
    db.rollback()

def get_sell_condition(active_user, db, models):
  try:
    possession_coins = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == active_user.idx).all()
    useTradingOption = db.query(models.tradingOption).filter(models.tradingOption.idx == active_user.trading_option).first()
    accountOtion = db.query(models.tradingAccountOption).filter(models.tradingAccountOption.idx == useTradingOption.idx).first()
    sellOption = db.query(models.tradingSellOption).filter(models.tradingSellOption.idx == useTradingOption.idx).first()
    return possession_coins, useTradingOption, accountOtion, sellOption
  except:
    db.rollback()

def get_rate_percent(nowWallet, possession):
  print("nowWallet ::: ",nowWallet)
  print("possession ::: ",possession)
  try:
    percent = (nowWallet / possession) * 100 - 100
  except Exception as e:
    print(e)
    percent = 0
  return percent