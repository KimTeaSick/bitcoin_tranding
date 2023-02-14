import mysql.connector
from dotenv import load_dotenv
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

