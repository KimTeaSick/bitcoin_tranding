import requests
import datetime
from collector.database import engine, SessionLocal
from sqlalchemy.orm import Session
import collector.models
import pandas as pd
from sqlalchemy import create_engine, desc

'''
try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

now1 = datetime.datetime.now()
coinList = db.query(collector.models.coinList).filter(collector.models.coinList.delflag == 0).all()



for coin in coinList:
    try:
        data = db.query(collector.models.coinMinPrice).filter(collector.models.coinMinPrice.coin_name == coin.coin_name).order_by(desc(collector.models.coinMinPrice.idx)).limit(100).all()
        #df = pd.read_sql(f"SELECT * FROM nc_p_min_bithumb_t where coin_name = '{coin.coin_name}' ORDER BY idx DESC LIMIT 100", con=engine)

        print(data[0].STime,data[0].coin_name)
    except Exception as e:
        print(e, coin.coin_name)



now2 = datetime.datetime.now()
print(now2-now1)
'''
class recommendCoin():
    def __init__(self):
        options = self.options
        return 'asdasd'