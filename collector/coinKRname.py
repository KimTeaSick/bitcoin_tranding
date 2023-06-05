from selenium import webdriver
from selenium.webdriver.common.by import By

# 웹 드라이버 설정
driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get('https://www.bithumb.com/coin_inout/compare_price')

# 모든 코인에 대한 웹 요소 가져오기
coinCrawl = driver.find_elements(By.XPATH, '//*[@id="tableAsset"]')

coins = coinCrawl[0].text

driver.quit()

print('----------------------------------------------------------------------------------------')
coins = coins.split('\n')

for coin in coins:
    if 'Mainnet' in coin:
        korName = coin.find('(')
        engName = coin.find(')')

        print(coin[:korName])
        print(coin[korName+1:engName])

        findKrName = coin.split()
        if len(findKrName) > 6:
            print(findKrName)
