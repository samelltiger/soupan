# coding=utf-8
import random
import urllib.request,urllib.error
import http.client

import lib.OpenPageFun as op

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

"""保存proxy到数据库"""
def proxySave(conn,data):
	if not len(data):
		return False

	count = 0
	for proxy in data:
		is_exist = conn.find({"proxy" : proxy}).count()
		if is_exist:
			continue

		dict_ip = {
			"proxy" : proxy,
			"status": 1
		}
		conn.insert_one(dict_ip)
		count += 1
		if count >= 70:
			break
	
	return count

"""从网页上获取代理ip列表，并保存至mongodb"""
def getProxyIpOfXiCi( mg_conn ):
    url = "http://www.xicidaili.com/wt/1"
    opener = op.getOpener({
        "User-Agent": getUserAgent()
    })
    resp = op.openPageWithCookie(opener,url)
    soup = op.getPageSoupByText(resp.read())
    tag_list = soup.select("#ip_list > tr > td")
    ips = tag_list[1::10]
    ports = tag_list[2::10]
    proxys = []

    for ip,port in zip(ips,ports):
	    proxys.append(ip.get_text()+":"+port.get_text())
    
    count = proxySave( mg_conn,proxys )
    return count

def get_proxy_ip(conn,status=0):
	data = conn.find({"status":status}).limit(1)
	proxy_list = list(data)

	if not len(proxy_list):
		return False

	return proxy_list[0]

def testProxy(conn):
	is_run = 1
	while is_run:
		# is_run = 0
		get_one_proxy = get_proxy_ip(conn,1)

		if not get_one_proxy:
			break

		proxy_support=urllib.request.ProxyHandler({'http':"http://"+get_one_proxy['proxy']})
		opener = urllib.request.build_opener(proxy_support)
		opener.addheaders = [("User-Agent", getUserAgent())]

		try:
			resp = opener.open("http://www.baidu.com/",None,timeout=3)
			conn.update({"_id":get_one_proxy["_id"]},{"$set":{"status":0}})
			
			print(get_one_proxy)
			
		except (urllib.error.URLError,http.client.RemoteDisconnected,ConnectionResetError,TimeoutError):
			conn.remove({"_id":get_one_proxy["_id"]})
			print("remove:",get_one_proxy)
			# print(err.args)
	