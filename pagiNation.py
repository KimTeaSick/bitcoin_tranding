from dbConnection import *
from sql import *
import math

class PagiNation:
    def orderListPageCount(self):
        count = Select(orderListCountSql)[0][0] / 12
        return math.ceil(count)