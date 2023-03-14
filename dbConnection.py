from dotenv import load_dotenv
import mysql.connector
import os 

load_dotenv()
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')



mydb = mysql.connector.connect(
    host = HOST,
    user = USERNAME,
    passwd = PASSWORD,
    database = DATABASE
)

def Insert( sql, val ):
    mycursor = mydb.cursor(prepared=True)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

def Select( sql ):
    mycursor = mydb.cursor(prepared=True)
    mycursor.execute(sql)
    result = mycursor.fetchall()
    selectData = []
    for data in result:
        selectData.append(data)
    mycursor.close()
    return selectData

