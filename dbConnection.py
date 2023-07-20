from dotenv import load_dotenv
import mysql.connector
from sqld import *

load_dotenv()

PORT = 3306
HOST = "nc-db-1.cyu1ow4eutwz.ap-northeast-2.rds.amazonaws.com"
DATABASE = "nc_bit_trading"
USERNAME = "admin"
PASSWORD = "$kim99bsd00"

class MySql():
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host = HOST,
                user = USERNAME,
                passwd = PASSWORD,
                database = DATABASE,
                port = PORT
            )
        except mysql.connector.Error as e:
            print('Database Error: ', e)
            self.Insert(insertLog,[e])


    def Insert( self, sql, val ):
        try:
            mycursor = self.mydb.cursor(prepared=True)
            mycursor.execute(sql, val)
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            self.mydb.reconnect()

    async def Update(self, sql, val ):
        try:
            mycursor = self.mydb.cursor(prepared=True)
            mycursor.execute(sql, val)
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            self.mydb.reconnect()    

    async def Delete(self, sql, val ):
        try:
            mycursor = self.mydb.cursor(prepared=True)
            mycursor.execute(sql, val)
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            self.mydb.reconnect()    
            
    async def AllDelete( self, sql ):
        try:
            mycursor = self.mydb.cursor(prepared=True)
            mycursor.execute(sql)
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            self.mydb.reconnect()    

    async def Select(self, sql ):
        try:
            mycursor = self.mydb.cursor(prepared=False)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            self.mydb.commit()
            selectData = []
            for data in result:
                selectData.append(data)
            mycursor.close()
            return selectData   
        except mysql.connector.Error as err:
            self.mydb.reconnect()
