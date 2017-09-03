import pymysql.cursors
import pymongo  

# import lib.OpenPageFun as op
from lib.OpenPageFun import getListFromDb

conn = pymysql.connect(host = 'localhost',
                        user = 'root',
                        password = '',
                        db  = 'soupan',
                        charset = 'utf8' ,
                        cursorclass=pymysql.cursors.DictCursor  #使返回的数据为dict格式
)

mgconn = pymongo.MongoClient("localhost",27017)
mgclient = mgconn['test']
mgtable = mgclient['list']


# sql = "select * from search_website"
# cursor = conn.cursor()
# cursor.execute(sql)
# result = cursor.fetchone()
# print(result['name'])
getListFromDb(conn,mgtable)