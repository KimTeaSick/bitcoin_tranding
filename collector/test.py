import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

now = datetime.datetime.now()
now2 = int(int(now.timestamp()) /60) * 60 + (60*540)

#unixtimestamp = 1685104320

#dbtime = datetime.datetime.utcfromtimestamp(unixtimestamp)

print(datetime.datetime.utcfromtimestamp(now2))
print(now2)

#findIndex = db.query(models.coinPrice1M).filter(models.coinPrice1M.S_time >= now2).first()

#print(findIndex.idx, findIndex.S_time, findIndex.time)