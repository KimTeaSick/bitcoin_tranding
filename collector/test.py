import pandas as pd

# 가상의 데이터 생성
data = pd.DataFrame({'Value': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})

# 4개씩 평균 계산
averages = data['Value'].rolling(window=4).mean()

print(averages)