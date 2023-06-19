import requests
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    db = SessionLocal()
    db: Session
finally:
    db.close()

# 코인 한국명 크롤링
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://www.bithumb.com/coin_inout/compare_price')

# 모든 코인에 대한 웹 요소 가져오기
coinCrawl = driver.find_elements(By.XPATH, '//*[@id="tableAsset"]')

coins = coinCrawl[0].text

driver.quit()

print('----------------------------------------------------------------------------------------')
coins = coins.split('\n')

coinNameList = []
coinNewName = []
warnning = []

for coin in coins:
    korName = coin.find('(')
    engName = coin.find(')')

    coinNameList.append(f'{coin[korName+1:engName]}_KRW')
    coinNewName.append({'coinEnglishName': f'{coin[korName+1:engName]}_KRW', 'coinKRName':coin[:korName]})

    if '투자유의종목' in coin:
        print(coin)
        warnning.append(f'{coin[korName+1:engName]}_KRW')

url = "https://api.bithumb.com/public/ticker/ALL_KRW"

headers = {"accept": "application/json"}
response = requests.get(url)
data = response.json()["data"]

coinlist1 = []
for dat in data:
    dat += '_KRW'
    coinlist1.append(dat)

coinlist2 = []
coinList = db.query(models.coinList).all()
for coin in coinList:
    coinlist2.append(coin.coin_name)

coinlist3 = list(set(coinlist1) - set(coinlist2))
coinlist4 = list(set(coinlist2) - set(coinlist1))

for coin in coinList:
    if coin.coin_name in coinlist4:
        coin.delflag = 1
    if coin.coin_name in warnning:
        coin.warning = '1'

print(warnning)

for coin in coinlist1:
    if coin == 'date_KRW':
        continue
    if coin not in coinlist2:
        try:
            print(coinNewName[coinNameList.index(coin)]['coinKRName'], coinNewName[coinNameList.index(coin)]['coinEnglishName'])
            newCoin = models.coinList()
            newCoin.coin_name = coin
            newCoin.delflag = 0
            newCoin.kr_name = coinNewName[coinNameList.index(coin)]['coinKRName']

            if coin in warnning:
                newCoin.warning = '1'
            else:
                newCoin.warning = '0'
            db.add(newCoin)

        except Exception as e:
            print(e)

db.commit()