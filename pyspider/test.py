# coding=utf-8
from bs4 import BeautifulSoup as bs
import urllib.request

resp = urllib.request.urlopen("https://movie.douban.com/")
# soup = bs(resp.read(),"lxml")
print(resp.read())
# data_list = soup.select("div.slide-page > a.item > p")
# print(data_list)