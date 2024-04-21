import json
import mysql.connector
import pymysql


class Config:
    def __init__(self):
        con_params = self.__read_config()
        self.db_conn = pymysql.connect(host=con_params["host"],
                                       user=con_params["user"],
                                       password=con_params["password"],
                                       db=con_params["db"],
                                       charset=con_params["charset"],
                                       cursorclass=pymysql.cursors.DictCursor)
    def __read_config(self):
        try:
            f = open("config.txt")
            data = f.read()
            return dict(json.loads(data))
        finally:
            f.close()