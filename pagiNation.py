from dbConnection import *
from sql import *
from dbConnection import MySql
import math

class PagiNation:

    def __init__(self):
        self.mysql = MySql()

    def orderListPageCount(self):
        count = self.mysql.Select(orderListCountSql)[0][0] / 12
        return math.ceil(count)