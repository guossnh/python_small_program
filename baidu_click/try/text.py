#-*- coding : utf-8 -*-
from selenium import webdriver
import time
import logging
import logging.config
import csv
from urllib import request
import json
import time
#下边 是变量
# Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0 
profileDir = "C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\witrfxpv.default"


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
    driver.get("http://sunchateau.com/free/UA.htm")
    time.sleep(5)
    driver.maximize_window()

    #driver.close()

#***************************************************变态的分割线*********************************************************

text2()



















