import lib.dbsFun as dbFun
import pymongo  

# import lib.OpenPageFun as op
'''自动搜索网站中的列表'''
import lib.OpenPageFun as op

conn = dbFun.getMysqlConnect('soupan')

mgclient = dbFun.getMongoConnect('test')
mgtable = mgclient('list')

# op.getListFromDb(conn,mgtable)

op.getSearchList(mgtable)

# sql = "select * from search_website"
# cursor = conn.cursor()
# cursor.execute(sql)
# result = cursor.fetchone()
# print(result['name'])