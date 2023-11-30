from dbConnection import MySql
from sql.dashBoardSql import *
import pandas as pd

class ChartMaker():
    def __init__(self):
        self.db = MySql()

    async def getChartData(self, idx, term):
        value = []
        rawChartData = await self.db.oneSelect(getChartDataSql(idx))
        chartData = pd.DataFrame(rawChartData)
        chartData = chartData.groupby(chartData.index // term).mean().round().astype(int)
        chartData = chartData.values.tolist()
        for data in chartData:
            value.append(data[0])
        return value