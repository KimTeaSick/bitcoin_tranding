from pymongo import MongoClient

class MongoDB():
    client = MongoClient("mongodb://192.168.10.204:27017/")
    mydb = client["nc_bit_trading"]
