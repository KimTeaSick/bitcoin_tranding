from dbConnection import *


def log(content):
  mysql = MySql()
  insertLog = "INSERT INTO nc_f_log_t (content, insert_date) VALUES (%s, now())" 
  mysql.Insert(insertLog,[content])