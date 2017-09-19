# coding=utf-8

'''获取数据库连接，MySQL和Mongodb'''
import pymysql.cursors
import pymongo  

'''连接到MySQL,并返回连接句柄'''
def getMysqlConnect(dbname):
    try:
        conn = pymysql.connect(
                            host = 'localhost',
                            db   = dbname,
                            user = 'root',
                            password = 'ct-sch',
                            charset = 'utf8',
                            cursorclass = pymysql.cursors.DictCursor
        )
        return conn
    except :
        print("数据库连接出错。")
        return False

'''连接到mongodb，返回一个存有连接的闭包，闭包参数为一个collection Name'''
def getMongoConnect(dbname):
    conn_client = pymongo.MongoClient('localhost',27017)
    db_link = conn_client[dbname]
    def getTable(tablename):
        if tablename=="close":
            conn_client.close()
            return True
        return db_link[tablename]
    return getTable