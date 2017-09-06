# coding=utf-8
import lib.dbsFun as dbFun

'''自动搜索网站中的列表'''
import lib.OpenPageFun as op

conn = dbFun.getMysqlConnect('soupan')
if not conn:
    print("数据库连接失败！")
    exit()

mgclient = dbFun.getMongoConnect('soupan')
mgtable = mgclient('keywords') # 保存从各个网站上获取到的搜索关键词，以及用户反馈的关键词

count = op.getListFromDb(conn,mgtable)

print(__file__,"time: ",op.getFormatTime(),'insert count:',count)
