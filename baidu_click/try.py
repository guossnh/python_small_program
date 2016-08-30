#-*- coding : utf-8 -*-

from selenium import webdriver
from urllib import request
from random import choice
import time , csv , json , time
import get_proxy , time
#下边 是变量
# Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0 
profileDir = "C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\witrfxpv.default"
#测试useragent 的网址 : http://www.sioe.cn/xinqing/UserAgent.php     http://sunchateau.com/free/UA.htm

def text1():
    global profileDir
    profile = webdriver.FirefoxProfile(profileDir)
    driver = webdriver.Firefox(profile)
    driver.get("https://www.baidu.com/s?wd=富硒六味地黄丸")
    assert "富硒六味地黄丸_百度搜索" in driver.title#确定页面是百度搜索页面
    driver.maximize_window()
    try:
        driver.find_element_by_partial_link_text("富硒六味地黄丸").click()
        print("find it ")
    except:
        print("no find")
    time.sleep(5)
    driver.quit()

def text2():
    global profileDir
    profile = webdriver.FirefoxProfile(profileDir)
    #设置useragent
    #profile.set_preference('general.useragent.override', "wocao")
    driver = webdriver.Firefox(profile)
    #driver.get("http://sunchateau.com/free/UA.htm")
    driver.get("http://baidu.com")
    #time.sleep(3)
    #driver.maximize_window()
    #设置 窗口 的大小
    driver.set_window_size(200 , 100)
    time.sleep(3)
    print("ok")

#这是读取browser.json文件 从而随机 获得一个useragent的值  用于 模拟浏览器
def text3(type):
    #读取json文件
    with open('../browser.json', 'r' , encoding="utf8") as f:
        data = json.load(f)
        wlist = data["phone_browser" if type == "phone" else "pc_browser"].values() 
        return choice(list(wlist))

#这个方法主要用于 测试python  读取配置文件的实例
def text4():
    with open('../config.json', 'r', encoding="utf8") as f:
        config = json.load(f)
        print(config['name'])




#***************************************************变态的分割线*********************************************************
#
text2()
#打印时间
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
#
#
#
#
#
#
#
#
#
#





def asd(abc):
    print(123)
    if abc:
        print("ok")
    else:
        print("else")
        asd(True)

#print(get_proxy.get())

# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# print(time.sleep(3))
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

