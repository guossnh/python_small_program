#更新一下 百度点击 的程序  需要增加 一些功能 
#gui 界面  ,exe 打包  关键词 用户 自己 添加  更改 这次 努力 完善一下 

#-*- coding : utf-8 -*-


#还是导包  真JB烦人  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time #导入时间包
import random #导入随机数包
import string #导入string包
import urllib
import binascii


#这里放一些变量
kewword = ""

baiduTitle = kewword + "_百度搜索"

driver = ""#= webdriver.Firefox()#确定浏览器

profile = webdriver.FirefoxProfile()#设置浏览器基本设置

#代理的两个变量  用于 计数
all_use_ip = 0
can_use_ip = 0

"""
下边是方法部分
"""

"""
这是 设置 代理的两个方法
""" 

#设置火狐浏览器的代理的办法,非常好用.得区分一下是不是https的链接
def setHttpsProxy(ip,port):#参数  ip地址   端口  类型   真为https 假为http
    global driver , profile#全局变量
    try:
        profile.set_preference('network.proxy.type', 1)#设置浏览器上完方式为手动
        #if 1==1:
        profile.set_preference('network.proxy.ssl', ip)
        profile.set_preference('network.proxy.ssl_port', port)
        #else:
        #    profile.set_preference('network.proxy.http', ip)
        #    profile.set_preference('network.proxy.http_port', port)
        profile.update_preferences()
        driver = webdriver.Firefox(profile)
        return True;
    except:
        return False;

def tryproxy():
    global all_use_ip , can_use_ip
    while True:
        all_use_ip = all_use_ip + 1 
        data = ''
        with urllib.request.urlopen('http://qsrdk.daili666api.com/ip/?tid=556258590050521&num=1&category=2&protocol=https&foreign=none&filter=on') as f:
            data = f.read().decode()
        proxy_handler = urllib.request.ProxyHandler({'https': data})
        proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
        try:
            wocao = opener.open('https://baidu.com')#测试链接是否可用
            print("链接正确")
            if wocao.status == 200:
                can_use_ip = can_use_ip + 1
                datalist = data.split(":")
                print("代理查找完毕,开始 设置浏览器代理")
                setHttpsProxy(datalist[0],datalist[1])
            else:
                pass
        except:
            time.sleep(3)
            print("链接出错,休息一下继续")

        print("总共检测ip为%s可用ip为%s"% all_use_ip,can_use_ip)




















#这个方法主要实现的是跳转到百度下一页 的页面.时间 的话   可以 根据 电脑 适当 的调节
def baiduNextPage():
    global baiduTitle , driver
    time.sleep(5)#等待页面载入
    assert baiduTitle in driver.title#确定页面是百度搜索页面
    driver.implicitly_wait(10)#隐试等待
    driver.execute_script("window.scrollBy(0,document.body.scrollHeight)","")#滚动到最下边.没什么卵用
    driver.find_element_by_link_text("下一页>").click()

#提供随机数  直接返回布尔值  默认为70%
def suiji(sum = 7):
    if int(random.uniform(0,10))<sum:
        return True
    else:
        return False

#主程序
def main():
    print(suiji())

if __name__ == '__main__':
    main()
