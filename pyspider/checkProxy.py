# coding=utf-8

import lib.OpenPageFun as op
import lib.proxyFun as proxy
import lib.dbsFun as dbFun

mgclient = dbFun.getMongoConnect('soupan')
# mgtable = mgclient('keywords') # 保存从各个网站上获取到的搜索关键词，以及用户反馈的关键词

'''爬取网盘搜索结果的列表，并保存到panduoduo'''
mg_save_proxy = mgclient('proxy')

"""测试代理ip是否有效"""
count = mg_save_proxy.find().count()
if count > 5:
    proxy.testProxy(mg_save_proxy)

print(__file__,"time: ",op.getFormatTime())