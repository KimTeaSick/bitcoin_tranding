from dbConnection import *
from sql import *
from dbConnection import MySql
import math

class PagiNation:

    def __init__(self):
        self.mysql = MySql()

    async def orderListPageCount(self):
        value = await self.mysql.Select(orderListCountSql)
        count = int(value[0][0]) / 14
        return round(count)