# coding=utf-8

import lib.OpenPageFun as op
import lib.proxyFun as proxy
import lib.dbsFun as dbFun

mgclient = dbFun.getMongoConnect('soupan')
mgtable = mgclient('keywords') # 保存从各个网站上获取到的搜索关键词，以及用户反馈的关键词

'''proxy ip的保存的表'''
mg_save_proxy = mgclient('proxy')

"""获取代理ip列表并保存"""
count = proxy.getProxyIpOfXiCi( mg_save_proxy )
proxy.testProxy(mg_save_proxy)

print(__file__,"time: ",op.getFormatTime(),'insert count：',count)