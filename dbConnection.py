from dotenv import load_dotenv
import mysql.connector
import asyncio
import os 

load_dotenv()
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


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

    async def Select(self, sql):
        try:
            mycursor = self.mydb.cursor(prepared=True)
            mycursor.execute(sql)
            result = mycursor.fetchall()
            selectData = []
            for data in result:
                selectData.append(data)
            mycursor.close()
            return selectData   
        except mysql.connector.Error as err:
            self.mydb.reconnect()   
