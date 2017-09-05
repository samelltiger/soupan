# coding=utf-8
import lib.dbsFun as dbFun

'''自动搜索网站中的列表'''
import lib.OpenPageFun as op

conn = dbFun.getMysqlConnect('soupan')

mgclient = dbFun.getMongoConnect('soupan')
mgtable = mgclient('keywords') # 保存从各个网站上获取到的搜索关键词，以及用户反馈的关键词

'''爬取网盘搜索结果的列表，并保存到panduoduo'''
mg_save_panduoduo = mgclient('panduoduo')
op.getSearchList(mgtable,mg_save_panduoduo)