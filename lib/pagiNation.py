from dbConnection import *
from sqld import *
from dbConnection import MySql

class PagiNation:
    def __init__(self):
        self.mysql = MySql()
        
    async def orderListPageCount(self):
        value = await self.mysql.Select(orderListCountSql)
        count = int(value[0][0]) / 14
        return round(count)