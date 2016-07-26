#这是一个美团网特定信息的爬虫程序,练手  就酱
#-*- coding : utf-8 -*-
#参考链接  http://cuiqingcai.com/1319.html    http://beautifulsoup.readthedocs.io/zh_CN/latest/


#导包
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
import re
#全局变量
#这是初始化数据库
conn = sqlite3.connect('meituan.db')
cursor = conn.cursor()
phone_zhengze=re.compile('1[3|5|7|8|][0-9]{9}')

citynamenum = 0 #用于计数,遍历整个

import time


#浏览器标识
headers  = {"User-Agent":"Mozilla/5.0 (Linux; Android 5.0.4; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"}

#man
#response = requests.get("http://i.meituan.com/beijing?cid=52&p=207")
#response = requests.get("http://www.meituan.com/api/v1/divisions")

"""
soup = BeautifulSoup(response.text , "lxml")
这也是其中的一种解析方式 都可以 正在使用的貌似 容错性会强.试试看吧
"""
#soup = BeautifulSoup(response.text , "html5lib")

#print(soup.find_all("span" , class_ = "poiname")[1].find_parent("a").get('href'))


#print(soup.find_all('id')[2].get_text())

#for x in soup.find_all('id'):
#    print(x.get_text())

#控制列表页面 的方法.
def meituan_list_page():
    while True:
        list_page_link = make_city_link()
        list_page_num = 1
        while True:
            #time.sleep(3)
            list_page_link2 = list_page_link+str(list_page_num)
            if find_none(list_page_link2):
                break
            else:
                return_number = do_list_page(list_page_link2)
                if return_number == 1:
                    list_page_num = int(list_page_num) + 1
                else:
                    break
        time.sleep(3)
        print("完成一个城市")

#传入一个链接然后处理页面数据
def do_list_page(page_link):
    global headers
    while True:
            try:
                list_page = requests.get(page_link , headers = headers)
                list_page_content = BeautifulSoup(list_page.text , "html5lib")
                break
            except:
                time.sleep(3)
    # list_page = requests.get(page_link)
    # list_page_content = BeautifulSoup(list_page.text , "html5lib")
    for x in list_page_content.find_all("span" , class_ = "poiname"):
        page_link=x.find_parent("a").get('href')
        save_date(page_link)
    #下边判断是不是最后一页
    try:
        request = list_page_content.find("div",class_ = "pager").find_all("a")[1].get("class")
        if request == ['btn', 'btn-weak', 'btn-disabled']:
            return 2
        else:
            return 1
    except:
        return 1


def make_city_link():
    global citynamenum
    city_link =  'http://i.meituan.com/%s?cid=52&p='% (get_city(citynamenum))
    return city_link


#这是一个判断页面是否有数据的办法.
def find_none(page_link):
    global headers
    print(page_link)
    try:
        try_page = requests.get(page_link , headers = headers)
        try_page_content = BeautifulSoup(try_page.text , "html5lib")
        # return False
    except :
        return False
    try:
        request = try_page_content.find("div",class_ = "no-deals").get_text()
        return True
    except:
        return False




#传入一个页面的链接  然后从页面 获取  需要的数据   然后存到数据库   就酱
def save_date(page_link):
    try:
        meituan_page = requests.get(page_link , headers = headers)
        meituan_date = BeautifulSoup(meituan_page.text , "html5lib")
        #time.sleep(1) #延长时间
        meiruan_name = meituan_date.find("h1", class_="dealcard-brand").get_text()
        meiruan_add = meituan_date.find("div", class_="poi-address").get_text()
        meituan_date.find("div", class_="kv-line-r").find("p").find("a").clear()#清除特殊的字符串
        meituan_all_phone = meituan_date.find("div", class_="kv-line-r").find("p").find("a").get("data-tele")
        #下边是一个电话处理的办法  找出手机号
        meituan_all_phone = meituan_all_phone.split("/")
        meituan_phone = ""
        meituan_phone2 = ""
        meituan_tel   = ""
        for x in meituan_all_phone:
            if phone_zhengze.match(str(x)) and meituan_phone != "":
                meituan_phone2 = x
            elif phone_zhengze.match(str(x)):
                meituan_phone = x
            else:
                meituan_tel = x
        link_sqllite(meiruan_name,"足疗按摩",page_link,meituan_phone,meituan_phone2,meituan_tel,meiruan_add)
    except:
        print("出现一个错误,休息1个时间")
        time.sleep(1)




def get_city(num):
    global citynamenum   #引入全局变量
    if num < 817:
        while True:
            try:
                file = requests.get("http://www.meituan.com/api/v1/divisions")
                cityname = BeautifulSoup(file.text , "html5lib")
                citynamenum = citynamenum + 1 #计数器加一
                print(cityname.find_all('id')[num].get_text())
                print("开始")
                #time.sleep(5)
                return cityname.find_all('id')[num].get_text()
                break
            except:
                time.sleep(2)

    else:
        sqlite_close()
        print("程序结束,都存到数据库了")
        os._exit(1)


"""
数据库部分  sqllite
"""

def link_sqllite(name,mtype,link,phone,phone2,tel,madd):
    cursor.execute("insert into meituandb (name,type,link,phone,phone2,tel,madd) values ('%s','%s','%s','%s','%s','%s','%s')" %(name,mtype,link,phone,phone2,tel,madd))
    conn.commit()


#关闭数据库
def sqlite_close():
    cursor.close()
    conn.close()



"""
下边是测试用的代码  不用的时候  记得注释    本来应该 写 man的 哎  再说吧
"""

meituan_list_page()


# meituan_page = requests.get("http://i.meituan.com/langfang?cid=52&p=1" , headers = headers)
# meituan_date = BeautifulSoup(meituan_page.text , "html5lib")
# print(meituan_page.text.encode("utf-8"))
