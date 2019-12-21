#-*- coding : utf-8 -*-

"""
这个主要是从微薄利寻找刷单的单子并且能够点击确定
"""
path_man_file = "C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"#主要浏览器的配置文件地址
weiboli_url = "http://www.vboly.com/web/activitymanager/managerActity/goodsid/507613.htm"
from selenium import webdriver


#打开chrome浏览器并且载入现在正在使用的配置

driver = webdriver.Chrome()

option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1")
driver = webdriver.Chrome(chrome_options=option)

driver.get(weiboli_url) # 获取百度页面

