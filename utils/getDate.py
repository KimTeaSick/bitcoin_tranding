import datetime 

def getTransactionTime():
  return datetime.datetime.now()

def getCancleTime(transactionTime, cancleTiem):
  return transactionTime + datetime.timedelta(seconds=cancleTiem)