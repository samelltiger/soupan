# coding=utf-8
from bs4 import BeautifulSoup as bs
import urllib.request,urllib.parse,urllib.error
import time
import json
import http.cookiejar
import random
import http.client

# 获取一个页面，返回urllib的响应
def getWebPage(url,data=None):
    request = urllib.request.Request(url,data)
    response = urllib.request.urlopen(request)
    return response

# 获取一个页面，返回BeautifulSoup对象
def getWebPageOfSoup(url,data=None):
    response = getWebPage(url,data=None)
    return bs(response.read().decode("utf-8"),'lxml')

"""通过文本创建一个soup对象"""
def getPageSoupByText(page_text):
    return bs(page_text,'lxml')

"""通过proxy获取web页面，并将不能打开页面的代理ip删掉，返回一个soup对象"""
def getPageByProxyOpener(url,proxy_conn):
    time.sleep(3)
    i = 0
    while 1:
        (proxy,opener) = getOpenerWithProxy( proxy_conn )
        
        if not opener:
            print("proxy总数为",proxy)
            exit()

        try:
            i += 1
            resp = openPageWithCookie(opener,url)
            return getPageSoupByText(resp.read())
        except (urllib.error.URLError,http.client.RemoteDisconnected,ConnectionResetError,TimeoutError):
            proxy_conn.remove({"_id":proxy["_id"]})
            if i == 3:
                return getWebPageOfSoup(url)

"""创建一个opener,并返回个cookie和opener"""
def getWebOpener(filename=None):
    cookie = http.cookiejar.MozillaCookieJar()
    if filename:
        cookie.load(filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    return (cookie,opener)

"""获取一个opener，带有user-agent和proxy"""
def getOpenerWithProxy( conn ):
    proxy = getProxyIp( conn )
    if not proxy:
        print("未获取到代理；")
        return (False,False)

    proxy_support = urllib.request.ProxyHandler({'http':"http://"+proxy['proxy']})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [("User-Agent", getUserAgent())]

    return (proxy,opener)

"""带有cookie信息打开页面"""
def openPageWithCookie(opener,url,data=None):
    page = opener.open(url,data)
    return page

# 通过节点的className从页面获取搜索数据(一个完整的页面)
def getDataByClass(page_data,classes,next_class=None):
    if not (len(classes) or isinstance(page_data,bs)):
        return False
    
    data = []
    for clas in classes:
        titles = page_data.select(clas)
        data.append([one.get_text().strip() for one in titles if len(one)])        
    return data

"""随机获取一个user-Agent"""
def getUserAgent():
    user_agent = [
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
  			'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
  			'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
  			'Sogou head spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
  			'Mozilla/4.0 (compatible; MSIE 5.0; Windows NT)',
  			'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
  			'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
  			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider',
  			'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
  			'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
  			'Sogou Pic Spider/3.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
  			'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
  			'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
  			'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
  			'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ;  QIHU 360EE)',
  			'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
  			'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) )',
  			'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
  			'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3',
    ]

    return user_agent[random.randint(0,18)]
"""随机获取一条代理Ip"""
def getProxyIp(conn):
    skip = conn.find().count()
    if not skip:
        print("代理总数为：" , skip)
        return False

    skip_num = random.randint(0,skip-1)
    data = conn.find().skip(skip_num).limit(1)
    proxy_list = list(data)

    if not len(proxy_list):
        print("未获取到代理ip，总数为：" , skip , "跳过的数目为：" ,  skip_num)
        return False

    return proxy_list[0]

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
            mg_conn.insert_one(dict_one)
            count += 1
    
    return count
            
'''主功能一：从mysql设置的网站中获取keywords'''
# 从数据库中依次查出url，并打开网页找出数据在存入另一数据库； 
def getListFromDb(fromMysqlServer,toMongoServer):
    fdb = fromMysqlServer
    tdb = toMongoServer
    get_sql = "SELECT id,url,category,classes,next_class,is_api FROM search_website WHERE status=1 limit 1"
    cursor = fdb.cursor()
    # cursor.execute(sql)
    # site_list = cursor.fetchone()

    total = 0
    is_run = 1
    while is_run:
        cursor.execute(get_sql)
        res = cursor.fetchone()
        if not res:
            is_run = 0
            # print("目前没有需要爬取的关键词！")
            break

        id = res['id']
        up_sql = "UPDATE search_website SET status=%d where id=%d"%(2,id)
        cursor.execute(up_sql)
        try:
            if res['is_api']:
                api_data = getWebPage(res['url']).read()
                data_list = json.loads(api_data.decode("utf-8"))
                data = getDataByApi(data_list,res['classes'].split(";"))
            else:
                soup = getWebPageOfSoup(res['url'])
                data = getDataByClass(soup,res['classes'].split(";"),res['next_class'])
            inset_count = savaToMongo(data,tdb,res['category'])
            total += inset_count
             

            up_sql = "UPDATE search_website SET status=%d where id=%d"%(0,id)
            cursor.execute(up_sql)
            #可以添加一个日志记录，记录该次运行时共插入了多少条数据
            # print("time: ",getFormatTime(),'insert count：',inset_count)


        except UnicodeEncodeError:
            print("time: ",getFormatTime(),"\tUnicodeEncodeError in",__file__)
    
    return total
    

'''获取当前的格式化时间'''
def getFormatTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

'''获取网页中表单的字段和token，并返回搜索的变量名和结果'''
def getInputName(soup):
    form = soup.select("#form1 > input")
    search_name = form[0].get("name")
    token_name = form[1].get("name")
    token = form[1].get("value")
    dict_res = {search_name:None,token_name:token}
    return (search_name ,dict_res)

'''主功能二：爬取网盘之家的搜索结果页面并存入数据库'''

'''从百度网盘之家获取网盘搜索列表地址'''
def getSearchList(mongo_conn , mongo_save , proxy_conn):
    url = "http://wowenda.com/"
    (cookie,opener) = getWebOpener(  )  #获取一个一面的cookie和opener
    resp = openPageWithCookie(opener,url)
    soup = getPageSoupByText(resp.read().decode("utf-8"))

    total = 0
    is_run = 1
    while(is_run):
        # is_run = 0  #测试时用
        title_list = mongo_conn.find({'status':1},{'_id':1,'title':1,'category':1}).limit(1)
        title = list(title_list)
        if not title:
            print("所有列表已爬取完成！")
            break

        title = title[0]

        (search_name,dict_res) = getInputName(soup)
        dict_res[search_name] = title['title']
        url_query = urllib.parse.urlencode(dict_res)
        mongo_conn.update({"_id":title['_id']},{"$set":{"status":2}})  #搜索正在处理的关键字状态更新为2
        
        for page_url in get100Page(opener,"search?r=0&"+url_query):
            print("获取的跳转页链接：",page_url)
            # soup = getWebPageOfSoup(url,url_query)
            run = 1
            while run:
                soup = getPageByProxyOpener(page_url,proxy_conn)
                list_res = soup.select("li.bt > a")
                list_sizes = soup.select("li > span:nth-of-type(1)")
                if len(list_res) or len(list_sizes):
                    print("以获取链接dom元素！" , list_res[0])
                    run = 0
            # page = openPageWithCookie(opener,page_url)
            # soup = getPageSoupByText(page.read().decode("utf-8"))
            # print(soup.prettify())
            
            titles = [i.get_text() for i in list_res]
            urls = [i['href'] for i in list_res]
            sizes = [i.get_text() for i in list_sizes]
            insert_count = saveListToMongo([titles,urls,sizes],mongo_save,title)
            total += insert_count
        
        mongo_conn.update({"_id":title['_id']},{"$set":{"status":0}})  #搜索已完成的关键字状态更新为0

    return total

"""主功能三：从盘多多获取真实的百度云资源链接"""
def getBaiduPanUrl(mg_conn,proxy_conn):
    is_run = 1
    count = 0

    while is_run:
        # is_run = 0
        title_list = mg_conn.find({'status':1},{'_id':1,'url':1}).limit(1)  # 爬取到盘多多地址但未得到百度云地址
        title = list(title_list)
        # print(title)
        if not len(title):
            break

        title = title[0]

        mg_conn.update({"_id":title['_id']},{"$set":{"status":2}})  # 正在获取百度云地址

        # soup = getWebPageOfSoup(title['url'])
        run = 1
        while run:
            soup = getPageByProxyOpener(title['url'],proxy_conn)
            next_url_tag = soup.select("div.m_down > a")
            
            if len(next_url_tag):
                print("已获取链接dom元素！", next_url_tag)
                run = 0

        next_url_tag = next_url_tag[0]
        next_url = next_url_tag['href']

        # soup = getWebPageOfSoup(next_url)
        run = 1
        while run:
            soup = getPageByProxyOpener(next_url,proxy_conn)
            org_url = soup.select("body > div > meta")
            if len(org_url):
                run = 0

        org_url = org_url[0]
        url = org_url['content']
        url = url[url.index("h"):]
        print("网盘地址：" , url)
        # print(title['_id'])
        
        mg_conn.update({"_id":title['_id']},{"$set":{"baidu_url":url,"status":3}})    # 保存百度云地址
        count += 1
    
    return count

"""将爬取结果存入wangpan 结果集"""
def saveListToMongo(data_list,mongo_save,line_record):
    count = 0
    for title,url,size in zip(data_list[0],data_list[1],data_list[2]):
        # 判断该记录是否在记录中已存在
        # is_exist = mongo_save.find({"title":title}).count()
        # if is_exist:
        #     continue
        line_dict = {
                "title" : title,
                "url"   : url,
                'category' : line_record['category'],
                "size"  : size.replace("资源大小：",""),
                "status" : 1,
                "useful": 1  # 是否可用
        }
        mongo_save.insert_one(line_dict)
        count += 1
    return count

"""获取网盘之家搜索结果的前100页"""
def get100Page(opener,url_query):
    url = "http://wowenda.com/"
    for i in range(1,100):
        yield url+url_query+"&page=%d"%(i)

'''设置带有header的opener'''
def getOpener(head):  
    # deal with the Cookies  
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)  
    header = []  
    for key, value in head.items():  
        elem = (key, value)  
        header.append(elem)  
    opener.addheaders = header  
    return opener  

# print(getWebPage("http://www.imooc.com").read())
# print(getWebPageOfSoup("http://www.imooc.com"))
