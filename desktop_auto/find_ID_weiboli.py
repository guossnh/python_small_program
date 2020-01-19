#-*- coding : utf-8 -*-
"""
这个主要是从微薄利寻找刷单的单子并且能够点击确定
"""
import time
from selenium import webdriver

path_man_file = "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"#主要浏览器的配置文件地址
weiboli_url = "http://www.vboly.com/web/activitymanager/managerActity/goodsid/507613.htm"
user_data = r"--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"   


#打开chrome浏览器并且载入现在正在使用的配置

option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
driver = webdriver.Chrome(chrome_options=option)
driver.get(weiboli_url)
assert "微薄利" in driver.title
time.sleep(5)


#from selenium.webdriver import ChromeOptions
#
#options = ChromeOptions()
#options.debugger_address = "127.0.0.1:" + '8888'
#browser = webdriver.Chrome(chrome_options=options,chrome_driver)
#browser.get("https://mms.pinduoduo.com/home/")
#assert "拼多多" in browser.title
#time.sleep(5)