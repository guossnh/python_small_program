#-*- coding : utf-8 -*-
#准备写一个检测店铺关注人数并且使用丁丁发送日报的程序.
from urllib import request
from selenium import webdriver
import time 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#这是全局变量
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
)
linkList = {'zhentou':'144074118'}
dblink = "D:\\git\\python_small_program\\AutoDingDingLog\\"
#http://shop.m.taobao.com/shop/shop_index.htm?shop_id=217495048       这是玛瑙店铺
#http://shop.m.taobao.com/shop/shop_index.htm?shop_id=144074118       这是枕头店铺


#通过传入店铺id获取这个页面的关注人数
def getFansNum(shopnum):
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver = webdriver.PhantomJS()
    driver.get('http://shop.m.taobao.com/shop/shop_index.htm?shop_id='+shopnum)
    assert "淘宝" in driver.title
    #driver.save_screenshot('C:\\Users\\Administrator\\Desktop\\screenshot.png')
    KeyWordList = driver.find_element_by_id("we-page").text.split("\n")
    FansNum = 0
    for i,e  in enumerate(KeyWordList):
        if e=="粉丝数":
            FansNum = KeyWordList[i-1]
    driver.close()
    return FansNum

#获取当天的数据存入下边文件,只要两个数据并且用#号隔开
def markFansMun():
    #print(getFansNum("217495048"))
    db = open(dblink+"dbfile.txt",'w')
    str = ""
    for k in linkList:
        str = str+linkList[k]+"#"
    db.write(str[:-1])
    db.close()

#主要是打开丁丁之后发送信息
def dingding():
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    driver.get('https://im.dingtalk.com/')
    time.sleep(5)
    driver.save_screenshot('C:\\Users\\Administrator\\Desktop\\screenshot.png')
    driver.close()
#主方法
def man():
    pass

dingding()