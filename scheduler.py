import schedule
import time 

def show():
  print(1)

def Insert1m():
  schedule.every(3).seconds.do(show)

def Insert5m():
  print(2)

def Insert1h():
  print(3)