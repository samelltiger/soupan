# coding=utf-8
from bs4 import BeautifulSoup as bs
import urllib.request
import time
import requests
import json

# 获取一个页面，返回urllib的响应
def getWebPage(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    return response

# 获取一个页面，返回BeautifulSoup对象
def getWebPageOfSoup(url):
    response = getWebPage(url)
    return bs(response.read(),'lxml')

# 通过节点的className从页面获取搜索数据(一个完整的页面)
def getDataByClass(page_data,classes,next_class=None):
    if not (len(classes) or isinstance(page_data,bs)):
        return False
    
    data = []
    for clas in classes:
        titles = page_data.select(clas)
        data.append([one.get_text().strip() for one in titles if len(one)])        
    return data

'''
获取api数据中的指定字段内容，dict_get中的索引为api的data存放字段（没有则为空），
从第二个开始，后面的是具体内容字段，第一个索引如果有则用分号间隔，多个要获取的索引用逗号分隔
'''
def getDataByApi(api_data,dict_get):
    if not len(dict_get):
        return False
    if not len(api_data):
        return False
    
    data = []
    if len(dict_get) == 1:
        index_all = dict_get[0].split(",")
        for one_data in api_data:
            data.append([one_data[index] for index in index_all])
    else:
        index_all = dict_get[1].split(",")
        for one_data in api_data[dict_get[0]]:
            data.append([one_data[index] for index in index_all])
    
    return data


# 将从网页中爬取的数据变成字典结构并存库,返回插入数据库的记录数
def savaToMongo(data,mg_conn,category):
    if not len(data):
        return False
    dict_data = []
    count=0
    for one_page in data:
        for title in one_page:
            is_exist = mg_conn.find({"title":title}).count()
            if is_exist:
                continue
            dict_one = {
                'title': title ,
                'category': category ,
                'status': 1 ,
            }
            # print(dict_one)
            mg_conn.insert_one(dict_one)
            count += 1
    
    return count
            

# 从数据库中依次查出url，并打开网页找出数据在存入另一数据库； 
def getListFromDb(fromMysqlServer,toMongoServer):
    fdb = fromMysqlServer
    tdb = toMongoServer
    sql = "SELECT url,category,classes,next_class,is_api FROM search_website WHERE status=1"
    cursor = fdb.cursor()
    cursor.execute(sql)
    site_list = cursor.fetchall()

    # print(tdb.find().count())
    for res in site_list:
        try:
            if res['is_api']:
                api_data = getWebPage(res['url']).read()
                data_list = json.loads(api_data.decode("utf-8"))
                data = getDataByApi(data_list,res['classes'].split(";"))
                # print(data)
            else:
                soup = getWebPageOfSoup(res['url'])
                data = getDataByClass(soup,res['classes'].split(";"),res['next_class'])
                # print(dict_data)
            dict_data = savaToMongo(data,toMongoServer,res['category'])
            print(data)
            print(dict_data)
            
        except UnicodeEncodeError:
            print("UnicodeEncodeError in",__file__,"line: ",__debug__)

# print(getWebPage("http://www.imooc.com").read())
# print(getWebPageOfSoup("http://www.imooc.com"))
