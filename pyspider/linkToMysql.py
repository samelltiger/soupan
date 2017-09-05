import lib.dbsFun as dbFun
import pymongo  

# import lib.OpenPageFun as op
'''自动搜索网站中的列表'''
import lib.OpenPageFun as op

# conn = dbFun.getMysqlConnect('soupan')

mgclient = dbFun.getMongoConnect('test')
# mgtable = mgclient('list')
# op.getListFromDb(conn,mgtable)

'''爬取网盘搜索结果的列表，并保存到panduoduo'''
mg_save_panduoduo = mgclient('panduoduo')
# op.getSearchList(mgtable,mg_save_panduoduo)


'''获取真实百度云url'''
print(op.getBaiduPanUrl(mg_save_panduoduo))
# sql = "select * from search_website"
# cursor = conn.cursor()
# cursor.execute(sql)
# result = cursor.fetchone()
# print(result['name'])