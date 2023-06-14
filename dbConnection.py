from dotenv import load_dotenv
import mysql.connector
import asyncio
import os 

load_dotenv()
PORT = "3306"
HOST = "192.168.10.202"
DATABASE = "nc_bit_trading"
USERNAME = "ipxnms"
PASSWORD = "$kim99bsd00"

class MySql():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = HOST,
            user = USERNAME,
            passwd = PASSWORD,
            database = DATABASE
        )

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
            selectData = []
            for data in result:
                selectData.append(data)
            mycursor.close()
            return selectData   
        except mysql.connector.Error as err:
            self.mydb.reconnect()
